"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function AdvisorCard({
    advisor,
}: Props) {

    const recommendation = advisor.recommendation;

    return (

        <div className="rounded-xl border p-6 shadow-sm transition-all hover:shadow-lg">

            <h2 className="text-lg font-semibold">

                AI Recommendation

            </h2>

            <div className="mt-6 space-y-4">

                <div className="text-4xl">

                    {recommendation.rating}

                </div>

                <div className="text-2xl font-bold">

                    {recommendation.recommendation}

                </div>

                <div className="text-5xl font-extrabold text-blue-600">

                    {recommendation.advisor_score}

                </div>

                {/* Progress Bar */}

                <div className="h-3 w-full rounded-full bg-slate-200 dark:bg-slate-700">

                    <div

                        className="h-3 rounded-full bg-blue-600 transition-all duration-700"

                        style={{

                            width: `${recommendation.advisor_score}%`,

                        }}

                    />

                </div>

                <div className="flex justify-between text-xs text-gray-500">

                    <span>0</span>

                    <span>50</span>

                    <span>100</span>

                </div>

                <div className="text-sm text-gray-500">

                    Score out of 100

                </div>

            </div>

        </div>

    );

}