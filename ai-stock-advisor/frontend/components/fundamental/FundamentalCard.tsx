"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function FundamentalCard({
    advisor,
}: Props) {

    const fundamental = advisor.engines.fundamental;

    const overall = fundamental.scores.overall;

    const recommendation = fundamental.recommendation;

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="text-lg font-semibold">

                Fundamental Analysis

            </h2>

            <div className="mt-6 space-y-4">

                <div className="text-4xl">

                    {recommendation.rating}

                </div>

                <div className="text-2xl font-bold">

                    {recommendation.recommendation}

                </div>

                <div className="text-5xl font-extrabold text-green-600">

                    {overall.overall_score}

                </div>

                <div className="text-sm text-gray-500">

                    Overall Financial Score

                </div>

            </div>

        </div>

    );

}