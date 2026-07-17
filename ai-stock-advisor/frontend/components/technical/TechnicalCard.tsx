"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function TechnicalCard({
    advisor,
}: Props) {

    const technical = advisor.engines.technical;

    const scores = technical.scores;

    const recommendation = technical.recommendation;

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="text-lg font-semibold">

                Technical Analysis

            </h2>

            <div className="mt-6 space-y-4">

                <div className="text-4xl">

                    {recommendation.rating}

                </div>

                <div className="text-2xl font-bold">

                    {recommendation.recommendation}

                </div>

                <div className="text-5xl font-extrabold text-blue-600">

                    {scores.technical_score}

                </div>

                <div className="text-sm text-gray-500">

                    Technical Score

                </div>

                <div className="pt-2 text-sm">

                    <span className="font-medium">
                        Grade:
                    </span>{" "}
                    {scores.grade}
                </div>

            </div>

        </div>

    );

}