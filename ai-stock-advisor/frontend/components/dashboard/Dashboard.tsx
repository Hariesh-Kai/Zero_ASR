"use client";

import SearchBar from "@/components/search/SearchBar";
import useAdvisor from "@/hooks/useAdvisor";
import CompanyCard from "@/components/company/CompanyCard";
import AdvisorCard from "@/components/advisor/AdvisorCard";
import RiskCard from "@/components/advisor/RiskCard";
import ConfidenceCard from "@/components/advisor/ConfidenceCard";
import FundamentalCard from "@/components/fundamental/FundamentalCard";
import TechnicalCard from "@/components/technical/TechnicalCard";
import NewsCard from "@/components/news/NewsCard";
import PriceChart from "@/components/chart/PriceChart";
import MetricsCard from "@/components/company/MetricsCard";
import SummaryCard from "@/components/advisor/SummaryCard";
import FinancialTabs from "@/components/financials/FinancialTabs";
import OverviewCard from "@/components/company/OverviewCard";
export default function Dashboard() {

    const {

        advisor,

        loading,

        error,

        loadAdvisor,

    } = useAdvisor();

    return (

        <div className="space-y-8">

            {/* Header */}

            <section>

                <h1 className="text-4xl font-bold">

                    AI Stock Advisor

                </h1>

                <p className="text-muted-foreground">

                    Intelligent stock analysis powered by AI.

                </p>

            </section>

            {/* Search */}

            <section className="rounded-xl border p-6">

                <SearchBar

                    onSelect={loadAdvisor}

                />

            </section>

            {

                loading && (

                    <p>

                        Loading advisor...

                    </p>

                )

            }

            {

                error && (

                    <p className="text-red-500">

                        {error}

                    </p>

                )

            }

            {

                advisor && (

                  <div className="space-y-6">

                      <CompanyCard advisor={advisor} />

                      <MetricsCard advisor={advisor} />

                      <OverviewCard advisor={advisor} />

                      <PriceChart ticker={advisor.ticker} />

                      <SummaryCard advisor={advisor} />

                      <div className="grid gap-6 lg:grid-cols-3">

                          <AdvisorCard advisor={advisor} />

                          <RiskCard advisor={advisor} />

                          <ConfidenceCard advisor={advisor} />

                      </div>

                      <div className="grid gap-6 lg:grid-cols-3">

                          <FundamentalCard advisor={advisor} />

                          <TechnicalCard advisor={advisor} />

                          <NewsCard advisor={advisor} />

                      </div>

                      <FinancialTabs
                            ticker={advisor.ticker}
                        />


                  </div>
              )

            }

        </div>

    );

}