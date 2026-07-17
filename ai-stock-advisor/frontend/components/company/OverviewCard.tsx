"use client";

import { AdvisorResponse } from "@/types/advisor";

interface Props {
    advisor: AdvisorResponse;
}

function formatNumber(value: number) {

    if (!value) return "-";

    return value.toLocaleString();

}

export default function OverviewCard({
    advisor,
}: Props) {

    const company = advisor.engines.fundamental.company;

    const items = [

        {
            label: "Exchange",
            value: company.exchange,
        },

        {
            label: "Sector",
            value: company.sector,
        },

        {
            label: "Industry",
            value: company.industry,
        },

        {
            label: "Country",
            value: company.country,
        },

        {
            label: "Employees",
            value: formatNumber(company.employees),
        },

        {
            label: "Currency",
            value: company.currency,
        },

        {
            label: "Average Volume",
            value: formatNumber(company.average_volume),
        },

        {
            label: "Shares Outstanding",
            value: formatNumber(company.shares_outstanding),
        },

    ];

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="mb-6 text-xl font-bold">

                🏢 Company Overview

            </h2>

            <div className="grid gap-4 md:grid-cols-2">

                {

                    items.map((item) => (

                        <div
                            key={item.label}
                            className="flex justify-between border-b pb-2"
                        >

                            <span className="text-muted-foreground">

                                {item.label}

                            </span>

                            <span className="font-semibold">

                                {item.value ?? "-"}

                            </span>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}