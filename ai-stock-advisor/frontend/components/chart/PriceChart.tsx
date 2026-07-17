"use client";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
} from "recharts";

import useChart from "@/hooks/useChart";

interface Props {
    ticker: string;
}

export default function PriceChart({
    ticker,
}: Props) {

    const {
        data,
        loading,
        error,
    } = useChart(ticker);

    if (loading) {

        return (

            <div className="rounded-xl border p-6">

                Loading Chart...

            </div>

        );

    }

    if (error) {

        return (

            <div className="rounded-xl border p-6 text-red-500">

                {error}

            </div>

        );

    }

    return (

        <div className="rounded-xl border p-6 shadow-sm">

            <h2 className="mb-6 text-xl font-semibold">

                Stock Price

            </h2>

            <ResponsiveContainer
                width="100%"
                height={350}
            >

                <LineChart data={data}>

                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                        dataKey="date"
                    />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="close"
                        stroke="#2563eb"
                        strokeWidth={2}
                        dot={false}
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>

    );

}