const API_BASE = "http://127.0.0.1:8000";

export async function searchCompanies(query: string) {

    const response = await fetch(

        `${API_BASE}/search?query=${encodeURIComponent(query)}`

    );

    if (!response.ok) {

        throw new Error("Search failed");

    }

    return response.json();

}

export async function getAdvisor(ticker: string) {

    const response = await fetch(
        `${API_BASE}/advisor/${ticker}`
    );

    if (!response.ok) {

        throw new Error("Failed to fetch advisor.");

    }

    return response.json();
}

export async function getChart(
    ticker: string,
    period = "6mo",
) {

    const response = await fetch(

        `${API_BASE}/chart/${ticker}?period=${period}`

    );

    if (!response.ok) {

        throw new Error(
            "Failed to fetch chart."
        );

    }

    return response.json();

}

export async function getFinancials(
    ticker: string,
) {

    const response = await fetch(

        `${API_BASE}/financials/${ticker}`

    );

    if (!response.ok) {

        throw new Error(
            "Failed to fetch financial statements."
        );

    }

    return response.json();

}