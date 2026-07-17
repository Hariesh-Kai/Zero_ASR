"use client";

import { useEffect, useState } from "react";

import { getFinancials } from "@/services/api";

export default function useFinancials(
    ticker: string,
) {

    const [data, setData] = useState<any>(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    useEffect(() => {

        async function load() {

            try {

                setLoading(true);

                setError("");

                const result = await getFinancials(
                    ticker,
                );

                setData(result);

            }

            catch (err) {

                console.error(err);

                setError(
                    "Failed to load financial statements."
                );

            }

            finally {

                setLoading(false);

            }

        }

        load();

    }, [ticker]);

    return {

        data,

        loading,

        error,

    };

}