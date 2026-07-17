export interface Recommendation {

    advisor_score: number;

    rating: string;

    recommendation: string;

    confidence: string;

}

export interface Confidence {

    confidence_score: number;

    confidence: string;

    engine_scores: number[];

}

export interface Risk {

    risk_score: number;

    risk_level: string;

}

export interface WeightingEngine {

    score: number;

    weight: number;

    weighted_score: number;

}

export interface Weighting {

    fundamental: WeightingEngine;

    technical: WeightingEngine;

    news: WeightingEngine;

    advisor_score: number;

}

export interface AdvisorResponse {

    engine: string;

    version: string;

    generated_at: string;

    ticker: string;

    advisor_score: number;

    summary: string;

    recommendation: Recommendation;

    confidence: Confidence;

    risk: Risk;

    weighting: Weighting;

    engines: any;

}