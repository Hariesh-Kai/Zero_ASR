import React, { useState, useEffect, useRef } from 'react';
import { 
  Mic, 
  Square, 
  UploadCloud, 
  Sparkles, 
  FileText, 
  Copy, 
  Check, 
  Trash2,
  HardDrive,
  Activity, 
  Volume2, 
  Languages,
  Zap,
  FolderOpen,
  Clock,
  CheckCircle2,
  AlertCircle,
  Loader2,
  RefreshCw,
  Download,
  X
} from 'lucide-react';
import { encodeWAV } from './utils/wavEncoder';

const API_BASE = 'http://127.0.0.1:8000';

export default function App() {
  // Backend & Model Info
  const [modelInfo, setModelInfo] = useState(null);
  const [backendOnline, setBackendOnline] = useState(false);
  const [isReloading, setIsReloading] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [trainingStatus, setTrainingStatus] = useState(null);

  // Active Modes & Settings
  const [activeTab, setActiveTab] = useState('mic'); // 'mic' | 'upload'
  const [mode, setMode] = useState('transcription'); // 'transcription' | 'clean'
  const [autoDelete, setAutoDelete] = useState(true); // Auto delete temp audio

  // Temp Folder State & Storage Drawer
  const [tempStats, setTempStats] = useState(null);
  const [showTempModal, setShowTempModal] = useState(false);
  const [showRomanizerModal, setShowRomanizerModal] = useState(false);

  // Recording State
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  // Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  // Transcription Output & Telemetry
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcriptionStage, setTranscriptionStage] = useState('idle'); // 'recording' | 'processing' | 'completed' | 'idle'
  const [result, setResult] = useState(null);
  const [copied, setCopied] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Tamil Interactive Playground
  const [tamilInput, setTamilInput] = useState('');
  const [romanizedResult, setRomanizedResult] = useState('');

  // History state
  const [history, setHistory] = useState([]);

  // Refs for Web Audio Recording
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const streamRef = useRef(null);
  const audioBuffersRef = useRef([]);
  const recordingActiveRef = useRef(false);
  const timerIntervalRef = useRef(null);
  const canvasRef = useRef(null);
  const analyserRef = useRef(null);
  const animationFrameRef = useRef(null);
  const fileInputRef = useRef(null);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3500);
  };

  // 1. Fetch Backend Info & Temp Stats
  const fetchInfo = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/info`);
      if (res.ok) {
        const data = await res.json();
        setModelInfo(data);
        setBackendOnline(true);
      } else {
        setBackendOnline(false);
      }
    } catch {
      setBackendOnline(false);
    }
  };

  const fetchTempStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/temp`);
      if (res.ok) {
        const data = await res.json();
        setTempStats(data);
      }
    } catch {
      // Ignore
    }
  };

  const fetchTrainingStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/training/status`);
      if (res.ok) {
        const data = await res.json();
        setTrainingStatus(data);
      }
    } catch {
      // Ignore if backend offline
    }
  };

  useEffect(() => {
    fetchInfo();
    fetchTempStats();
    fetchTrainingStatus();
    const interval = setInterval(() => {
      fetchInfo();
      fetchTempStats();
      fetchTrainingStatus();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Hot Reload Model Checkpoint
  const handleReloadModel = async () => {
    setIsReloading(true);
    try {
      const res = await fetch(`${API_BASE}/api/reload`, { method: 'POST' });
      if (res.ok) {
        const data = await res.json();
        showToast(`Model reloaded: ${data.checkpoint} (${(data.parameters / 1e6).toFixed(1)}M params)`);
        await fetchInfo();
      } else {
        showToast('Model reload request failed');
      }
    } catch (err) {
      showToast('Error connecting to backend reload: ' + err.message);
    } finally {
      setIsReloading(false);
    }
  };

  // Clear Temp Folder Action
  const handleClearTemp = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/clear_temp`, { method: 'POST' });
      if (res.ok) {
        await fetchTempStats();
        await fetchInfo();
        showToast('Temp folder cleared successfully');
      }
    } catch (err) {
      setErrorMsg('Failed to clear temp folder: ' + err.message);
    }
  };

  // Delete Single Temp File
  const handleDeleteSingleFile = async (filename) => {
    try {
      const res = await fetch(`${API_BASE}/api/temp/${filename}`, { method: 'DELETE' });
      if (res.ok) {
        await fetchTempStats();
        await fetchInfo();
        showToast(`Deleted ${filename}`);
      }
    } catch (err) {
      setErrorMsg('Failed to delete file: ' + err.message);
    }
  };

  // 2. High-Fidelity 16kHz PCM WAV Microphone Recording
  const startRecording = async () => {
    setErrorMsg('');
    setResult(null);
    audioBuffersRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx({ sampleRate: 16000 });
      audioContextRef.current = ctx;

      if (ctx.state === 'suspended') {
        await ctx.resume();
      }

      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 64;
      analyserRef.current = analyser;
      source.connect(analyser);

      drawVisualizer();

      const processor = ctx.createScriptProcessor(4096, 1, 1);
      processorRef.current = processor;

      recordingActiveRef.current = true;
      setIsRecording(true);
      setTranscriptionStage('recording');
      setRecordingTime(0);

      processor.onaudioprocess = (e) => {
        if (!recordingActiveRef.current) return;
        const inputData = e.inputBuffer.getChannelData(0);
        audioBuffersRef.current.push(new Float32Array(inputData));
      };

      source.connect(processor);
      processor.connect(ctx.destination);

      timerIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 0.1);
      }, 100);
    } catch (err) {
      recordingActiveRef.current = false;
      setIsRecording(false);
      setTranscriptionStage('idle');
      setErrorMsg('Microphone access error: ' + err.message);
    }
  };

  const stopRecording = () => {
    if (!recordingActiveRef.current) return;
    recordingActiveRef.current = false;
    setIsRecording(false);
    clearInterval(timerIntervalRef.current);
    cancelAnimationFrame(animationFrameRef.current);

    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
    }
    if (processorRef.current) {
      processorRef.current.disconnect();
    }

    const totalLength = audioBuffersRef.current.reduce((acc, b) => acc + b.length, 0);

    if (totalLength > 1600) {
      const mergedSamples = new Float32Array(totalLength);
      let offset = 0;
      for (const buf of audioBuffersRef.current) {
        mergedSamples.set(buf, offset);
        offset += buf.length;
      }

      const wavBlob = encodeWAV(mergedSamples, 16000);
      setAudioBlob(wavBlob);
      const url = URL.createObjectURL(wavBlob);
      setAudioUrl(url);
      sendAudioForTranscription(wavBlob, 'mic_recording.wav');
    } else {
      setErrorMsg('Recording was too short. Speak for at least 1 second.');
      setTranscriptionStage('idle');
    }
  };

  const drawVisualizer = () => {
    if (!analyserRef.current || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const bufferLength = analyserRef.current.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      animationFrameRef.current = requestAnimationFrame(render);
      analyserRef.current.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / bufferLength) * 1.5;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height * 0.85;
        const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
        gradient.addColorStop(0, '#6366f1');
        gradient.addColorStop(1, '#06b6d4');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, canvas.height - barHeight, barWidth - 2, barHeight);
        x += barWidth;
      }
    };
    render();
  };

  // 3. Audio File Drop & Upload
  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      processSelectedFile(e.target.files[0]);
    }
  };

  const processSelectedFile = (file) => {
    setErrorMsg('');
    setResult(null);
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setAudioUrl(url);
    sendAudioForTranscription(file, file.name);
  };

  // 4. Transcription API Request
  const sendAudioForTranscription = async (fileOrBlob, filename) => {
    setIsProcessing(true);
    setTranscriptionStage('processing');
    setErrorMsg('');

    const formData = new FormData();
    formData.append('file', fileOrBlob, filename);
    formData.append('mode', mode);
    formData.append('auto_delete', String(autoDelete));

    try {
      const response = await fetch(`${API_BASE}/api/transcribe`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({ detail: 'Transcription server error' }));
        throw new Error(errData.detail || `Server status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setTranscriptionStage('completed');
      setHistory((prev) => [
        {
          id: Date.now(),
          text: data.text,
          lang: data.language,
          time: new Date().toLocaleTimeString(),
          rtf: data.speedup,
        },
        ...prev.slice(0, 9),
      ]);
      fetchTempStats();
    } catch (err) {
      setErrorMsg(err.message);
      setTranscriptionStage('idle');
    } finally {
      setIsProcessing(false);
    }
  };

  // Copy to clipboard
  const handleCopy = () => {
    if (result && result.text) {
      navigator.clipboard.writeText(result.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Download Transcript TXT
  const handleDownload = () => {
    if (!result || !result.text) return;
    const element = document.createElement('a');
    const file = new Blob([result.text], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `transcription_${Date.now()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  // Tamil Romanizer Test
  const handleRomanizeTest = async () => {
    if (!tamilInput) return;
    try {
      const res = await fetch(`${API_BASE}/api/romanize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: tamilInput }),
      });
      if (res.ok) {
        const data = await res.json();
        setRomanizedResult(data.romanized);
      }
    } catch {
      // Fallback
    }
  };

  return (
    <div className="app-container">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="toast-notification">
          <CheckCircle2 size={18} color="#6366f1" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* App Header */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-icon-wrapper">
            <Activity size={22} />
          </div>
          <div className="brand-info">
            <h1>Antigravity ASR</h1>
            <p>Conformer-CTC Speech AI • English & Romanized Tamil</p>
          </div>
        </div>

        <div className="header-telemetry">
          <div className={`telemetry-pill ${backendOnline ? 'online' : ''}`}>
            <span className={`status-dot ${backendOnline ? '' : 'offline'}`} />
            <span>{backendOnline ? (modelInfo?.device_name || 'GPU Active') : 'Backend Offline'}</span>
          </div>

          {modelInfo && (
            <div className="telemetry-pill">
              <span>{(modelInfo.parameters / 1e6).toFixed(1)}M params</span>
              <span style={{ color: 'var(--text-muted)' }}>•</span>
              <span style={{ color: 'var(--accent-cyan)' }}>{modelInfo.checkpoint}</span>
            </div>
          )}

          <button 
            className="btn-header-action"
            onClick={handleReloadModel}
            disabled={isReloading}
            title="Reload latest trained checkpoint"
          >
            <RefreshCw size={14} className={isReloading ? 'animate-spin' : ''} />
            <span>{isReloading ? 'Reloading...' : 'Reload'}</span>
          </button>

          <button 
            className="btn-header-action"
            onClick={() => setShowTempModal(true)}
            title="Inspect temp directory storage"
          >
            <HardDrive size={14} />
            <span>K:\ASR\temp ({tempStats?.file_count || 0})</span>
          </button>

          <button 
            className="btn-header-action"
            onClick={() => setShowRomanizerModal(true)}
            title="Tamil Script Romanizer Tool"
          >
            <Languages size={14} />
            <span>Tamil Tool</span>
          </button>
        </div>
      </header>

      {/* Training Progress Banner */}
      {trainingStatus?.has_checkpoint && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          background: 'rgba(99, 102, 241, 0.08)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          borderRadius: 'var(--radius-md)',
          padding: '10px 18px',
          marginBottom: 16,
          fontSize: '0.83rem',
        }}>
          <Loader2 size={15} color="var(--accent-indigo)" style={{ animation: 'spin 2s linear infinite', flexShrink: 0 }} />
          <span style={{ color: 'var(--accent-indigo)', fontWeight: 600 }}>Training in Progress</span>
          <span style={{ color: 'var(--text-secondary)' }}>
            Epoch {trainingStatus.epoch} • Loss {trainingStatus.loss} • {trainingStatus.size_mb}MB checkpoint
          </span>
          <span style={{ marginLeft: 'auto', color: 'var(--text-muted)' }}>
            Reload model when done → click <strong>Reload</strong> button above
          </span>
        </div>
      )}

      {/* Main Studio Grid */}
      <main className="studio-grid">
        {/* Left Column: Audio Capture Deck */}
        <section className="studio-card">
          <div className="card-header">
            <div className="card-title">
              <Volume2 size={18} color="var(--accent-indigo)" />
              <span>Audio Studio</span>
            </div>
          </div>

          {/* Segmented Mode Switcher */}
          <div className="segmented-control">
            <button 
              className={`segmented-btn ${activeTab === 'mic' ? 'active' : ''}`}
              onClick={() => setActiveTab('mic')}
            >
              <Mic size={15} />
              <span>Microphone</span>
            </button>
            <button 
              className={`segmented-btn ${activeTab === 'upload' ? 'active' : ''}`}
              onClick={() => setActiveTab('upload')}
            >
              <UploadCloud size={15} />
              <span>File Import</span>
            </button>
          </div>

          {/* Microphone Capture View */}
          {activeTab === 'mic' && (
            <div className="record-deck">
              <div className="record-btn-container">
                {!isRecording ? (
                  <button 
                    className="record-main-btn"
                    onClick={startRecording}
                    title="Click to start recording"
                  >
                    <Mic size={34} />
                  </button>
                ) : (
                  <button 
                    className="record-main-btn recording"
                    onClick={stopRecording}
                    title="Click to stop and transcribe"
                  >
                    <Square size={28} />
                  </button>
                )}
              </div>

              <div className="timer-tag">
                {isRecording ? `${recordingTime.toFixed(1)}s` : '00:00'}
              </div>

              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                {isRecording ? 'Listening... Speak into microphone' : 'Click the button to record speech'}
              </p>

              <canvas ref={canvasRef} className="waveform-canvas" width={380} height={50} />
            </div>
          )}

          {/* File Upload View */}
          {activeTab === 'upload' && (
            <div>
              <div 
                className={`file-dropzone ${isDragging ? 'dragging' : ''}`}
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleFileDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="dropzone-icon">
                  <UploadCloud size={24} />
                </div>
                <h5 style={{ fontSize: '0.9rem', marginBottom: 4 }}>
                  {selectedFile ? selectedFile.name : 'Drop audio file or click to browse'}
                </h5>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  Supports WAV, FLAC, MP3, WebM, OGG
                </p>
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileInputChange} 
                  accept="audio/*" 
                  style={{ display: 'none' }} 
                />
              </div>
            </div>
          )}

          {/* Audio Player Preview */}
          {audioUrl && (
            <div className="audio-player-card" style={{ marginBottom: 20 }}>
              <audio controls src={audioUrl} />
            </div>
          )}

          {/* Settings & Configuration Deck */}
          <div className="settings-group">
            <div className="setting-row">
              <div className="setting-info">
                <h5>Post-Processing Mode</h5>
                <p>Clean formatting & punctuation vs verbatim CTC raw</p>
              </div>
              <select 
                value={mode} 
                onChange={(e) => setMode(e.target.value)}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-medium)',
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.8rem'
                }}
              >
                <option value="transcription">Standard (Punctuation)</option>
                <option value="clean">Clean (No disfluencies)</option>
              </select>
            </div>

            <div className="setting-row">
              <div className="setting-info">
                <h5>Auto-Delete Temp Audio</h5>
                <p>Purge temporary files from K:\ASR\temp after recognition</p>
              </div>
              <label className="toggle-switch">
                <input 
                  type="checkbox" 
                  checked={autoDelete} 
                  onChange={(e) => setAutoDelete(e.target.checked)} 
                />
                <span className="toggle-slider" />
              </label>
            </div>
          </div>
        </section>

        {/* Right Column: Transcription Output Console */}
        <section className="studio-card transcription-console">
          {/* Stage Status Bar */}
          <div className="status-stage-bar">
            <div className="stage-badge">
              {transcriptionStage === 'recording' && (
                <>
                  <span className="status-dot" style={{ backgroundColor: 'var(--accent-rose)', boxShadow: '0 0 8px var(--accent-rose)' }} />
                  <span style={{ color: 'var(--accent-rose)' }}>Recording Audio Stream...</span>
                </>
              )}
              {transcriptionStage === 'processing' && (
                <>
                  <Loader2 size={15} className="animate-spin" color="var(--accent-cyan)" />
                  <span style={{ color: 'var(--accent-cyan)' }}>Conformer-CTC Decoding...</span>
                </>
              )}
              {transcriptionStage === 'completed' && (
                <>
                  <CheckCircle2 size={15} color="var(--accent-emerald)" />
                  <span style={{ color: 'var(--accent-emerald)' }}>Transcription Ready</span>
                </>
              )}
              {transcriptionStage === 'idle' && (
                <>
                  <span className="status-dot" style={{ backgroundColor: 'var(--text-muted)' }} />
                  <span style={{ color: 'var(--text-secondary)' }}>Ready for audio input</span>
                </>
              )}
            </div>

            {result && (
              <div style={{ display: 'flex', gap: 8 }}>
                <span className="telemetry-pill" style={{ padding: '4px 10px', fontSize: '0.75rem', borderColor: 'var(--accent-indigo)' }}>
                  {result.language}
                </span>
                <span className="telemetry-pill" style={{ padding: '4px 10px', fontSize: '0.75rem', borderColor: 'var(--accent-cyan)' }}>
                  {result.speedup}x Real-Time
                </span>
              </div>
            )}
          </div>

          {/* Error Banner */}
          {errorMsg && (
            <div style={{
              background: 'rgba(244, 63, 94, 0.1)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              borderRadius: 'var(--radius-md)',
              padding: '12px 16px',
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              color: '#fca5a5',
              fontSize: '0.85rem'
            }}>
              <AlertCircle size={18} />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Main Output Display */}
          <div className="output-panel">
            {result?.text ? (
              <div>
                <div className="output-text-area">{result.text}</div>
                {result.raw_text && result.raw_text !== result.text.toLowerCase() && (
                  <div style={{ marginTop: 14, paddingTop: 14, borderTop: '1px dashed var(--border-subtle)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>CTC Raw: </span>
                    <code>{result.raw_text}</code>
                  </div>
                )}
              </div>
            ) : isProcessing ? (
              <div className="output-empty">
                <Loader2 size={36} className="animate-spin" color="var(--accent-indigo)" />
                <p>Generating acoustic transcript...</p>
              </div>
            ) : (
              <div className="output-empty">
                <FileText size={36} />
                <p>Your transcription results will appear here</p>
              </div>
            )}

            {/* Metrics Footer */}
            {result && (
              <div className="metrics-bar">
                <div className="metric-card">
                  <div className="metric-label">Audio Length</div>
                  <div className="metric-value">{result.duration_sec}s</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Latency</div>
                  <div className="metric-value">{result.latency_ms}ms</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">RTF Ratio</div>
                  <div className="metric-value">{result.rtf}</div>
                </div>
                <div className="metric-card">
                  <div className="metric-label">Storage</div>
                  <div className="metric-value" style={{ fontSize: '0.85rem', color: result.auto_deleted ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
                    {result.auto_deleted ? 'Auto-Deleted' : 'Saved to Temp'}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          {result?.text && (
            <div className="output-actions">
              <button className="btn-action" onClick={handleCopy}>
                {copied ? <Check size={14} color="var(--accent-emerald)" /> : <Copy size={14} />}
                <span>{copied ? 'Copied!' : 'Copy Text'}</span>
              </button>
              <button className="btn-action" onClick={handleDownload}>
                <Download size={14} />
                <span>Download .txt</span>
              </button>
            </div>
          )}

          {/* Quick History List */}
          {history.length > 0 && (
            <div style={{ marginTop: 10 }}>
              <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Recent Sessions
              </h5>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                {history.slice(0, 3).map((item) => (
                  <div 
                    key={item.id} 
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      background: 'var(--bg-surface-elevated)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '8px 12px',
                      fontSize: '0.8rem'
                    }}
                  >
                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '70%' }}>
                      {item.text}
                    </span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{item.time}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </main>

      {/* Temp Directory Inspector Modal */}
      {showTempModal && (
        <div className="modal-overlay" onClick={() => setShowTempModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <HardDrive size={18} color="var(--accent-indigo)" />
                <h4>Storage Inspector (K:\ASR\temp)</h4>
              </div>
              <button className="btn-header-action" onClick={() => setShowTempModal(false)}>
                <X size={16} />
              </button>
            </div>

            <div className="modal-body">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Total Files: <strong>{tempStats?.file_count || 0}</strong> • Size: <strong>{((tempStats?.total_size_bytes || 0) / 1024).toFixed(1)} KB</strong>
                </span>
                <button 
                  className="btn-action" 
                  onClick={handleClearTemp}
                  style={{ color: 'var(--accent-rose)' }}
                  disabled={!tempStats?.files?.length}
                >
                  <Trash2 size={14} />
                  <span>Purge All Files</span>
                </button>
              </div>

              {tempStats?.files?.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {tempStats.files.map((file) => (
                    <div 
                      key={file.name} 
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        background: 'var(--bg-surface)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '10px 14px',
                        fontSize: '0.85rem'
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: 500 }}>{file.name}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {(file.size_bytes / 1024).toFixed(1)} KB • {new Date(file.created_time * 1000).toLocaleTimeString()}
                        </div>
                      </div>
                      <button 
                        className="btn-action" 
                        onClick={() => handleDeleteSingleFile(file.name)}
                        style={{ padding: '4px 8px' }}
                      >
                        <Trash2 size={14} color="var(--accent-rose)" />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '30px 0', color: 'var(--text-muted)' }}>
                  No temporary audio files in K:\ASR\temp
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Tamil Romanizer Playground Modal */}
      {showRomanizerModal && (
        <div className="modal-overlay" onClick={() => setShowRomanizerModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <Languages size={18} color="var(--accent-cyan)" />
                <h4>Tamil Script Romanizer Playground</h4>
              </div>
              <button className="btn-header-action" onClick={() => setShowRomanizerModal(false)}>
                <X size={16} />
              </button>
            </div>

            <div className="modal-body">
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 16 }}>
                Type or paste Tamil Unicode script below to view the non-translated phonetic Romanization:
              </p>
              <textarea 
                value={tamilInput}
                onChange={(e) => setTamilInput(e.target.value)}
                placeholder="எ.கா: நான் இன்னைக்கு வீட்டுக்கு போறேன்"
                rows={3}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-medium)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px',
                  fontSize: '0.95rem',
                  marginBottom: 12
                }}
              />
              <button className="btn-action primary" onClick={handleRomanizeTest} style={{ marginBottom: 16 }}>
                <Sparkles size={14} />
                <span>Romanize Phonetically</span>
              </button>

              {romanizedResult && (
                <div style={{ background: 'var(--bg-surface)', padding: 14, borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: 4 }}>Output:</div>
                  <div style={{ fontSize: '1.1rem', color: 'var(--accent-cyan)', fontFamily: 'var(--font-mono)' }}>{romanizedResult}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
