"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

export default function NewsCard({
    advisor,
}: Props) {

    const news = advisor.engines.news;

    const recommendation = news.recommendation;

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="text-lg font-semibold">

                News Analysis

            </h2>

            <div className="mt-6 space-y-4">

                <div className="text-4xl">

                    {recommendation.rating}

                </div>

                <div className="text-2xl font-bold">

                    {recommendation.recommendation}

                </div>

                <div className="text-5xl font-extrabold text-orange-500">

                    {recommendation.news_score}

                </div>

                <div className="text-sm text-gray-500">

                    News Score

                </div>

                <div className="pt-2 text-sm">

                    <span className="font-medium">
                        Confidence:
                    </span>{" "}
                    {recommendation.confidence}
                </div>

            </div>

        </div>

    );

}