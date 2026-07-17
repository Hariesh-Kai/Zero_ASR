"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function SummaryCard({
    advisor,
}: Props) {

    return (

        <div className="rounded-xl border p-6 shadow-sm space-y-6">

            <h2 className="text-2xl font-bold">

                🧠 AI Investment Summary

            </h2>

            {/* Top Statistics */}

            <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">

                <div className="rounded-lg border p-4">

                    <p className="text-sm text-gray-500">

                        Recommendation

                    </p>

                    <p className="mt-2 text-xl font-bold">

                        {advisor.recommendation.recommendation}

                    </p>

                </div>

                <div className="rounded-lg border p-4">

                    <p className="text-sm text-gray-500">

                        Overall Score

                    </p>

                    <p className="mt-2 text-xl font-bold text-blue-600">

                        {advisor.advisor_score.toFixed(1)}/100

                    </p>

                </div>

                <div className="rounded-lg border p-4">

                    <p className="text-sm text-gray-500">

                        Risk

                    </p>

                    <p className="mt-2 text-xl font-bold text-orange-500">

                        {advisor.risk.risk_level}

                    </p>

                </div>

                <div className="rounded-lg border p-4">

                    <p className="text-sm text-gray-500">

                        Confidence

                    </p>

                    <p className="mt-2 text-xl font-bold text-green-600">

                        {advisor.confidence.confidence}

                    </p>

                </div>

            </div>

            {/* AI Summary */}

            <div>

                <h3 className="mb-2 text-lg font-semibold">

                    AI Analysis

                </h3>

                <p className="leading-8 text-gray-600 dark:text-gray-300">

                    {advisor.summary}

                </p>

            </div>

        </div>

    );

}