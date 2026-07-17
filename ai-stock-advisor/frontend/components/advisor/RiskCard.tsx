"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function RiskCard({
    advisor,
}: Props) {

    const risk = advisor.risk;

    function getRiskColor(level: string) {

        switch (level.toLowerCase()) {

            case "low":
                return "text-green-600";

            case "medium":
                return "text-yellow-600";

            case "high":
                return "text-red-600";

            default:
                return "text-gray-600";
        }
    }

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="text-lg font-semibold">

                Risk Analysis

            </h2>

            <div className="mt-6 space-y-4">

                <p
                    className={`text-3xl font-bold ${getRiskColor(
                        risk.risk_level
                    )}`}
                >
                    {risk.risk_level}
                </p>

                <p className="text-5xl font-extrabold">

                    {risk.risk_score}

                </p>

                {/* Progress Bar */}

                <div className="h-3 w-full rounded-full bg-slate-200 dark:bg-slate-700">

                    <div

                        className="h-3 rounded-full bg-orange-500 transition-all duration-700"

                        style={{

                            width: `${risk.risk_score}%`,

                        }}

                    />

                </div>

                <div className="flex justify-between text-xs text-gray-500">

                    <span>0</span>

                    <span>50</span>

                    <span>100</span>

                </div>

                <p className="text-sm text-gray-500">

                    Risk Score

                </p>

            </div>

        </div>

    );

}