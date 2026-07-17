"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function ConfidenceCard({
    advisor,
}: Props) {

    const confidence = advisor.confidence;

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="text-lg font-semibold">

                Confidence

            </h2>

            <div className="mt-6 space-y-4">

                <p className="text-3xl font-bold">

                    {confidence.confidence}

                </p>

                <p className="text-5xl font-extrabold text-green-600">

                    {confidence.confidence_score}%

                </p>

                {/* Progress Bar */}

                <div className="h-3 w-full rounded-full bg-slate-200 dark:bg-slate-700">

                    <div

                        className="h-3 rounded-full bg-green-600 transition-all duration-700"

                        style={{

                            width: `${confidence.confidence_score}%`,

                        }}

                    />

                </div>

                <div className="flex justify-between text-xs text-gray-500">

                    <span>0</span>

                    <span>50</span>

                    <span>100</span>

                </div>

                <p className="text-sm text-gray-500">

                    Model Confidence

                </p>

            </div>
        </div>

    );

}