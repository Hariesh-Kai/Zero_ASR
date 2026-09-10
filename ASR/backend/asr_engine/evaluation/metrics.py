"""
Evaluation Metrics Module for ASR.
Computes:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Detailed alignment breakdown (Substitutions, Deletions, Insertions)
- Real-Time Factor (RTF)
"""

from typing import List, Tuple, Dict, Any, Union
import time


def compute_levenshtein(ref_tokens: List[str], hyp_tokens: List[str]) -> Tuple[int, int, int, int]:
    """
    Computes Levenshtein distance using Dynamic Programming.
    Returns: (distance, substitutions, deletions, insertions)
    """
    n, m = len(ref_tokens), len(hyp_tokens)
    # dp[i][j] = (dist, s, d, ins)
    dp = [[(0, 0, 0, 0) for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = (i, 0, i, 0)  # i deletions
    for j in range(1, m + 1):
        dp[0][j] = (j, 0, 0, j)  # j insertions

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                sub = (dp[i - 1][j - 1][0] + 1, dp[i - 1][j - 1][1] + 1, dp[i - 1][j - 1][2], dp[i - 1][j - 1][3])
                dele = (dp[i - 1][j][0] + 1, dp[i - 1][j][1], dp[i - 1][j][2] + 1, dp[i - 1][j][3])
                ins = (dp[i][j - 1][0] + 1, dp[i][j - 1][1], dp[i][j - 1][2], dp[i][j - 1][3] + 1)
                dp[i][j] = min(sub, dele, ins, key=lambda x: x[0])

    return dp[n][m]


def compute_wer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Computes Word Error Rate: (S + D + I) / N.
    Supports single string or list of strings (corpus-level evaluation).
    """
    if isinstance(reference, list) and isinstance(hypothesis, list):
        total_dist = 0
        total_s = 0
        total_d = 0
        total_i = 0
        total_ref_len = 0
        for r, h in zip(reference, hypothesis):
            r_words = r.strip().lower().split()
            h_words = h.strip().lower().split()
            if not r_words:
                total_i += len(h_words)
                total_dist += len(h_words)
                continue
            dist, s, d, ins = compute_levenshtein(r_words, h_words)
            total_dist += dist
            total_s += s
            total_d += d
            total_i += ins
            total_ref_len += len(r_words)

        wer = total_dist / max(1, total_ref_len)
        return {
            "wer": wer,
            "substitutions": total_s,
            "deletions": total_d,
            "insertions": total_i,
            "ref_length": total_ref_len,
        }

    ref_words = reference.strip().lower().split()
    hyp_words = hypothesis.strip().lower().split()

    if not ref_words:
        return {
            "wer": 0.0 if not hyp_words else 1.0,
            "substitutions": 0,
            "deletions": 0,
            "insertions": len(hyp_words),
            "ref_length": 0,
        }

    dist, s, d, i = compute_levenshtein(ref_words, hyp_words)
    wer = dist / len(ref_words)
    return {
        "wer": wer,
        "substitutions": s,
        "deletions": d,
        "insertions": i,
        "ref_length": len(ref_words),
    }


def compute_cer(reference: Union[str, List[str]], hypothesis: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Computes Character Error Rate: (S + D + I) / N.
    Supports single string or list of strings (corpus-level evaluation).
    """
    if isinstance(reference, list) and isinstance(hypothesis, list):
        total_dist = 0
        total_s = 0
        total_d = 0
        total_i = 0
        total_ref_len = 0
        for r, h in zip(reference, hypothesis):
            r_chars = list(r.strip().lower())
            h_chars = list(h.strip().lower())
            if not r_chars:
                total_i += len(h_chars)
                total_dist += len(h_chars)
                continue
            dist, s, d, ins = compute_levenshtein(r_chars, h_chars)
            total_dist += dist
            total_s += s
            total_d += d
            total_i += ins
            total_ref_len += len(r_chars)

        cer = total_dist / max(1, total_ref_len)
        return {
            "cer": cer,
            "substitutions": total_s,
            "deletions": total_d,
            "insertions": total_i,
            "ref_length": total_ref_len,
        }

    ref_chars = list(reference.strip().lower())
    hyp_chars = list(hypothesis.strip().lower())

    if not ref_chars:
        return {
            "cer": 0.0 if not hyp_chars else 1.0,
            "substitutions": 0,
            "deletions": 0,
            "insertions": len(hyp_chars),
            "ref_length": 0,
        }

    dist, s, d, i = compute_levenshtein(ref_chars, hyp_chars)
    cer = dist / len(ref_chars)
    return {
        "cer": cer,
        "substitutions": s,
        "deletions": d,
        "insertions": i,
        "ref_length": len(ref_chars),
    }


def compute_rtf(audio_duration_seconds: float, inference_time_seconds: float) -> float:
    """
    Computes Real-Time Factor (RTF = inference_time / audio_duration).
    RTF < 1.0 means faster than real-time.
    """
    if audio_duration_seconds <= 0:
        return 0.0
    return inference_time_seconds / audio_duration_seconds
