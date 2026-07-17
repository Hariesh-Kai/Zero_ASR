"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

function formatMarketCap(value: number) {

    if (value >= 1_000_000_000_000)
        return `$${(value / 1_000_000_000_000).toFixed(2)}T`;

    if (value >= 1_000_000_000)
        return `$${(value / 1_000_000_000).toFixed(2)}B`;

    if (value >= 1_000_000)
        return `$${(value / 1_000_000).toFixed(2)}M`;

    return `$${value}`;
}

export default function MetricsCard({
    advisor,
}: Props) {

    const company = advisor.engines.fundamental.company;
    const metrics = [

        {
            icon: "💲",
            title: "Current Price",
            value: `$${company.current_price}`,
        },

        {
            icon: "🏢",
            title: "Market Cap",
            value: formatMarketCap(company.market_cap),
        },

        {
            icon: "📊",
            title: "P/E Ratio",
            value: company.pe_ratio,
        },

        {
            icon: "💵",
            title: "EPS",
            value: company.eps,
        },

        {
            icon: "💰",
            title: "Dividend",
            value: `${company.dividend_yield}%`,
        },

        {
            icon: "📈",
            title: "52W High",
            value: `$${company.fifty_two_week_high}`,
        },

        {
            icon: "📉",
            title: "52W Low",
            value: `$${company.fifty_two_week_low}`,
        },

    ];
    return (

        <div className="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-7">

            {

                metrics.map((metric) => (

                    <div
                        key={metric.title}
                        className="rounded-xl border bg-card p-5 shadow-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-lg"
                    >

                        <div className="flex items-center justify-between">

                            <span className="text-2xl">

                                {metric.icon}

                            </span>

                        </div>

                        <p className="mt-4 text-sm text-muted-foreground">

                            {metric.title}

                        </p>

                        <p className="mt-2 text-2xl font-bold">

                            {metric.value}

                        </p>

                    </div>

                ))

            }

        </div>

    );

}