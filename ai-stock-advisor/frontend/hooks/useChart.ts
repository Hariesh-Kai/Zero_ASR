"use client";

import { useEffect, useState } from "react";

import { getChart } from "@/services/api";

export interface ChartPoint {
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
}

export default function useChart(
    ticker: string,
    period: string = "6mo",
) {
    const [data, setData] = useState<ChartPoint[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {

        async function load() {

            try {

                setLoading(true);
                setError("");

                const chart = await getChart(
                    ticker,
                    period,
                );

                setData(chart);

            } catch (err) {

                console.error(err);
                setError("Failed to load chart.");

            } finally {

                setLoading(false);

            }

        }

        load();

    }, [ticker, period]);

    return {
        data,
        loading,
        error,
    };
}