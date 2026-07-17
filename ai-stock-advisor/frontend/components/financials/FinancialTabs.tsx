"use client";

import { useState } from "react";

import useFinancials from "@/hooks/useFinancials";

import IncomeStatement from "./IncomeStatement";
import BalanceSheet from "./BalanceSheet";
import CashFlow from "./CashFlow";

interface Props {

    ticker: string;

}

export default function FinancialTabs({

    ticker,

}: Props) {

    const {

        data,

        loading,

        error,

    } = useFinancials(ticker);

    const [

        tab,

        setTab,

    ] = useState("income");

    if (loading)
        return <p>Loading financials...</p>;

    if (error)
        return <p>{error}</p>;

    if (!data)
        return null;

    return (

        <div className="rounded-xl border p-6">

            <div className="mb-6 flex rounded-xl border bg-slate-100 p-1 dark:bg-slate-800">

                <button
                    onClick={() => setTab("income")}
                    className={`flex-1 rounded-lg px-4 py-2 transition-all ${
                        tab === "income"
                            ? "bg-white font-semibold shadow dark:bg-slate-700"
                            : "hover:bg-slate-200 dark:hover:bg-slate-700"
                    }`}
                >
                    Income Statement
                </button>

                <button
                    onClick={() => setTab("balance")}
                    className={`flex-1 rounded-lg px-4 py-2 transition-all ${
                        tab === "balance"
                            ? "bg-white font-semibold shadow dark:bg-slate-700"
                            : "hover:bg-slate-200 dark:hover:bg-slate-700"
                    }`}
                >
                    Balance Sheet
                </button>

                <button
                    onClick={() => setTab("cash")}
                    className={`flex-1 rounded-lg px-4 py-2 transition-all ${
                        tab === "cash"
                            ? "bg-white font-semibold shadow dark:bg-slate-700"
                            : "hover:bg-slate-200 dark:hover:bg-slate-700"
                    }`}
                >
                    Cash Flow
                </button>

            </div>

            {
                tab === "income" &&
                <IncomeStatement
                    data={data.income_statement}
                />
            }

            {
                tab === "balance" &&
                <BalanceSheet
                    data={data.balance_sheet}
                />
            }

            {
                tab === "cash" &&
                <CashFlow
                    data={data.cash_flow}
                />
            }

        </div>

    );

}