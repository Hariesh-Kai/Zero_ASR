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

export default function CompanyCard({
    advisor,
}: Props) {

    const company = advisor.engines.fundamental.company;

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-2xl font-bold">

                        {company.name}

                    </h2>

                    <p className="text-sm text-gray-500">

                        {advisor.ticker}

                    </p>

                </div>

            </div>

            <div className="mt-6 grid grid-cols-2 gap-6">

                <div>

                    <p className="text-sm text-gray-500">

                        Sector

                    </p>

                    <p className="font-semibold">

                        {company.sector}

                    </p>

                </div>

                <div>

                    <p className="text-sm text-gray-500">

                        Industry

                    </p>

                    <p className="font-semibold">

                        {company.industry}

                    </p>

                </div>

                <div>

                    <p className="text-sm text-gray-500">

                        Country

                    </p>

                    <p className="font-semibold">

                        {company.country}

                    </p>

                </div>

                <div>

                    <p className="text-sm text-gray-500">

                        Market Cap

                    </p>

                    <p className="font-semibold">

                        {formatMarketCap(company.market_cap)}

                    </p>

                </div>

            </div>

        </div>

    );

}