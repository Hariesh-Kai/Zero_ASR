"use client";

import { useState } from "react";

import { getAdvisor } from "@/services/api";

import { AdvisorResponse } from "@/types/advisor";

export default function useAdvisor() {

    const [advisor, setAdvisor] = useState<AdvisorResponse | null>(null);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState<string | null>(null);

    async function loadAdvisor(
        ticker: string,
    ) {

        try {

            setLoading(true);

            setError(null);

            const data = await getAdvisor(
                ticker,
            );

            setAdvisor(data);

        }

        catch (err) {

            setError("Failed to load advisor.");

            console.error(err);

        }

        finally {

            setLoading(false);

        }

    }

    return {

        advisor,

        loading,

        error,

        loadAdvisor,

    };

}