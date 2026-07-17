"use client";

import { useEffect, useState } from "react";

import { searchCompanies } from "@/services/api";

import { CompanySearchResult } from "@/types/company";

interface Props {

    onSelect: (

        ticker: string,

    ) => void;

}

export default function SearchBar({

    onSelect,

}: Props) {

    const [query, setQuery] = useState("");

    const [results, setResults] = useState<
        CompanySearchResult[]
    >([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (query.length < 2) {

            setResults([]);

            return;

        }

        const timer = setTimeout(async () => {

            try {

                setLoading(true);

                const data = await searchCompanies(query);

                setResults(data);

            }

            catch (err) {

                console.error(err);

            }

            finally {

                setLoading(false);

            }

        }, 400);

        return () => clearTimeout(timer);

    }, [query]);

    return (

        <div className="relative">

            <input

                className="w-full rounded-lg border bg-background px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
                
                placeholder="Search companies..."

                value={query}

                onChange={(e) =>

                    setQuery(e.target.value)

                }

            />

            {

                loading && (

                    <p className="mt-2 text-sm">

                        Searching...

                    </p>

                )

            }

            {

                results.length > 0 && (

                    <div className="absolute z-50 mt-2 w-full rounded-lg border bg-white shadow-lg dark:bg-slate-900">

                        {

                            results.map((company) => (

                                <button

                                    key={company.symbol}

                                    type="button"

                                    className="flex w-full items-center justify-between px-4 py-3 text-left hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors border-b last:border-b-0"
                                    
                                    onClick={() => {

                                        onSelect(company.symbol);

                                        setQuery(company.symbol);

                                        setResults([]);

                                    }}

>

                                    <div>

                                        <div className="font-semibold">

                                            {company.symbol}

                                        </div>

                                        <div className="text-sm text-gray-500">

                                            {company.name}

                                        </div>

                                    </div>

                                    <div className="text-xs">

                                        {company.exchange}

                                    </div>

                                </button>

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}