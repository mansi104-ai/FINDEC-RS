'use client'

import { FormEvent, useMemo, useState } from 'react'
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from 'recharts'

import styles from './page.module.css'
import {
  evaluateSuitability,
  SuitabilityRequest,
  SuitabilityResponse,
} from '@/utils/api'

const initialForm: SuitabilityRequest = {
  age: 31,
  income_level: 'medium',
  monthly_income: 90000,
  monthly_expenses: 50000,
  income_stability: 'stable',
  investment_experience: 'intermediate',
  financial_literacy_level: 'moderate',
  current_holdings: [
    { name: 'Large Cap Fund', sector: 'diversified', value: 180000 },
    { name: 'Tech Growth Fund', sector: 'technology', value: 60000 },
  ],
  current_holdings_value: 240000,
  liabilities: 120000,
  emergency_fund_months: 5,
  financial_goal: 'long_term_wealth_creation',
  time_horizon_years: 8,
  liquidity_needs: 'medium',
  return_expectations: 'balanced',
  volatility_comfort: 3,
  drawdown_tolerance: 3,
  return_preference: 'balanced',
}

const fieldOptions = {
  income_level: ['low', 'medium', 'high'],
  income_stability: ['low', 'variable', 'medium', 'stable'],
  investment_experience: ['beginner', 'intermediate', 'advanced'],
  financial_literacy_level: ['basic', 'moderate', 'advanced'],
  financial_goal: [
    'long_term_wealth_creation',
    'retirement',
    'short_term_savings',
    'learning_based_exploratory_investing',
    'passive_investing',
    'active_stock_selection',
  ],
  liquidity_needs: ['low', 'medium', 'high'],
  return_expectations: ['steady', 'balanced', 'high_upside'],
  return_preference: ['steady', 'balanced', 'high_upside'],
} as const

function formatLabel(value: string) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (char: string) => char.toUpperCase())
}

function getLabelTone(label: string) {
  if (label === 'high_fit') return styles.highTone
  if (label === 'medium_fit') return styles.mediumTone
  return styles.lowTone
}

export default function Home() {
  const [form, setForm] = useState<SuitabilityRequest>(initialForm)
  const [results, setResults] = useState<SuitabilityResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const topRecommendation = results?.recommendations[0] ?? null

  const metrics = useMemo(() => {
    const savings = Math.max(form.monthly_income - form.monthly_expenses, 0)
    const savingsRate = form.monthly_income > 0 ? Math.round((savings / form.monthly_income) * 100) : 0
    const liquidityScore = { low: 35, medium: 65, high: 90 }[form.liquidity_needs] ?? 50
    const literacyScore = { basic: 35, moderate: 65, advanced: 88 }[form.financial_literacy_level] ?? 50
    const horizonScore = Math.min(Math.round((form.time_horizon_years / 12) * 100), 100)

    return {
      savings,
      savingsRate,
      radar: [
        { metric: 'Risk', value: form.volatility_comfort * 20 },
        { metric: 'Drawdown', value: form.drawdown_tolerance * 20 },
        { metric: 'Horizon', value: horizonScore },
        { metric: 'Liquidity', value: liquidityScore },
        { metric: 'Savings', value: Math.min(savingsRate * 2, 100) },
        { metric: 'Literacy', value: literacyScore },
      ],
    }
  }, [
    form.drawdown_tolerance,
    form.financial_literacy_level,
    form.liquidity_needs,
    form.monthly_expenses,
    form.monthly_income,
    form.time_horizon_years,
    form.volatility_comfort,
  ])

  const setField = <K extends keyof SuitabilityRequest>(key: K, value: SuitabilityRequest[K]) => {
    setForm((current) => ({ ...current, [key]: value }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await evaluateSuitability(form)
      setResults(response)
    } catch {
      setError('Backend unavailable on port 8000.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <form className={styles.formCard} onSubmit={handleSubmit}>
          <div className={styles.headerRow}>
            <div>
              <p className={styles.kicker}>Investor Brief</p>
              <h1>Financial Fit Dashboard</h1>
            </div>
            <button className={styles.primaryButton} type="submit" disabled={loading}>
              {loading ? 'Running...' : 'Run'}
            </button>
          </div>

          <div className={styles.formGrid}>
            <label>
              <span>Age</span>
              <input type="number" min="18" max="100" value={form.age} onChange={(event) => setField('age', Number(event.target.value))} />
            </label>
            <label>
              <span>Income Level</span>
              <select value={form.income_level} onChange={(event) => setField('income_level', event.target.value)}>
                {fieldOptions.income_level.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Monthly Income</span>
              <input type="number" min="0" value={form.monthly_income} onChange={(event) => setField('monthly_income', Number(event.target.value))} />
            </label>
            <label>
              <span>Monthly Expenses</span>
              <input type="number" min="0" value={form.monthly_expenses} onChange={(event) => setField('monthly_expenses', Number(event.target.value))} />
            </label>
            <label>
              <span>Income Stability</span>
              <select value={form.income_stability} onChange={(event) => setField('income_stability', event.target.value)}>
                {fieldOptions.income_stability.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Experience</span>
              <select value={form.investment_experience} onChange={(event) => setField('investment_experience', event.target.value)}>
                {fieldOptions.investment_experience.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Literacy</span>
              <select value={form.financial_literacy_level} onChange={(event) => setField('financial_literacy_level', event.target.value)}>
                {fieldOptions.financial_literacy_level.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Holdings Value</span>
              <input type="number" min="0" value={form.current_holdings_value} onChange={(event) => setField('current_holdings_value', Number(event.target.value))} />
            </label>
            <label>
              <span>Liabilities</span>
              <input type="number" min="0" value={form.liabilities} onChange={(event) => setField('liabilities', Number(event.target.value))} />
            </label>
            <label>
              <span>Emergency Fund</span>
              <input type="number" min="0" step="0.5" value={form.emergency_fund_months} onChange={(event) => setField('emergency_fund_months', Number(event.target.value))} />
            </label>
            <label>
              <span>Goal</span>
              <select value={form.financial_goal} onChange={(event) => setField('financial_goal', event.target.value)}>
                {fieldOptions.financial_goal.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Horizon</span>
              <input type="number" min="1" step="0.5" value={form.time_horizon_years} onChange={(event) => setField('time_horizon_years', Number(event.target.value))} />
            </label>
            <label>
              <span>Liquidity</span>
              <select value={form.liquidity_needs} onChange={(event) => setField('liquidity_needs', event.target.value)}>
                {fieldOptions.liquidity_needs.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Return Expectation</span>
              <select value={form.return_expectations} onChange={(event) => setField('return_expectations', event.target.value)}>
                {fieldOptions.return_expectations.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>Volatility Comfort</span>
              <input type="range" min="1" max="5" value={form.volatility_comfort} onChange={(event) => setField('volatility_comfort', Number(event.target.value))} />
              <strong>{form.volatility_comfort}</strong>
            </label>
            <label>
              <span>Drawdown Tolerance</span>
              <input type="range" min="1" max="5" value={form.drawdown_tolerance} onChange={(event) => setField('drawdown_tolerance', Number(event.target.value))} />
              <strong>{form.drawdown_tolerance}</strong>
            </label>
            <label>
              <span>Return Preference</span>
              <select value={form.return_preference} onChange={(event) => setField('return_preference', event.target.value)}>
                {fieldOptions.return_preference.map((option) => (
                  <option key={option} value={option}>
                    {formatLabel(option)}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className={styles.miniStats}>
            <article>
              <span>Savings</span>
              <strong>{metrics.savings}</strong>
            </article>
            <article>
              <span>Savings Rate</span>
              <strong>{metrics.savingsRate}%</strong>
            </article>
            <article>
              <span>Risk Band</span>
              <strong>
                {results?.risk_profile.final_risk_band
                  ? formatLabel(String(results.risk_profile.final_risk_band))
                  : '-'}
              </strong>
            </article>
            <article>
              <span>Preferred Asset</span>
              <strong>
                {results?.preference_profile?.preferred_asset_type
                  ? formatLabel(String(results.preference_profile.preferred_asset_type))
                  : '-'}
              </strong>
            </article>
          </div>

          {error ? <p className={styles.errorBanner}>{error}</p> : null}
        </form>

        <section className={styles.resultsPanel}>
          <div className={styles.radarCard}>
            <div className={styles.cardTitleRow}>
              <div>
                <span className={styles.kicker}>Radar</span>
                <h2>Risk and Intent Profile</h2>
              </div>
              <span className={`${styles.scorePill} ${getLabelTone(topRecommendation?.suitability_label ?? 'low_fit')}`}>
                {topRecommendation ? formatLabel(topRecommendation.suitability_label) : 'Ready'}
              </span>
            </div>
            <div className={styles.chartFrame}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={metrics.radar} outerRadius="72%">
                  <PolarGrid stroke="var(--chart-grid)" />
                  <PolarAngleAxis
                    dataKey="metric"
                    tick={{ fill: 'var(--chart-text)', fontSize: 12, fontWeight: 700 }}
                  />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar
                    name="Profile"
                    dataKey="value"
                    stroke="var(--chart-stroke)"
                    fill="var(--chart-fill)"
                    fillOpacity={0.45}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div className={styles.topMeta}>
              <article>
                <span>Top Match</span>
                <strong>{topRecommendation?.name ?? 'Run brief'}</strong>
              </article>
              <article>
                <span>Score</span>
                <strong>{Math.round(topRecommendation?.suitability_score ?? 0)}</strong>
              </article>
              <article>
                <span>Risk Band</span>
                <strong>
                  {results?.risk_profile.final_risk_band
                    ? formatLabel(String(results.risk_profile.final_risk_band))
                    : '-'}
                </strong>
              </article>
              <article>
                <span>Content Match</span>
                <strong>{Math.round(topRecommendation?.content_match_score ?? 0)}</strong>
              </article>
            </div>
          </div>

          <div className={styles.recommendationStack}>
            {results?.engine_summary ? (
              <article className={styles.summaryCard}>
                <span className={styles.kicker}>Brief</span>
                <p>{results.engine_summary}</p>
              </article>
            ) : null}

            {(results?.recommendations ?? []).map((recommendation) => (
              <article key={recommendation.recommendation_id} className={styles.recommendationCard}>
                <div className={styles.recommendationHeader}>
                  <h3>{recommendation.name}</h3>
                  <div className={`${styles.scoreBadge} ${getLabelTone(recommendation.suitability_label)}`}>
                    {Math.round(recommendation.suitability_score)}
                  </div>
                </div>
                <div className={styles.metaGrid}>
                  <article>
                    <span>Type</span>
                    <strong>{recommendation.asset_type}</strong>
                  </article>
                  <article>
                    <span>Confidence</span>
                    <strong>{recommendation.confidence_score.toFixed(2)}</strong>
                  </article>
                  <article>
                    <span>Content Match</span>
                    <strong>{Math.round(recommendation.content_match_score)}</strong>
                  </article>
                  <article>
                    <span>Action</span>
                    <strong>{recommendation.next_best_action}</strong>
                  </article>
                </div>
                <div className={styles.listBlock}>
                  <h4>Warnings</h4>
                  <ul>
                    {recommendation.risk_warnings.map((warning) => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </div>
              </article>
            ))}
          </div>

          {results?.rejected_alternatives?.length ? (
            <div className={styles.rejectedCard}>
              <span className={styles.kicker}>Rejected</span>
              <div className={styles.rejectedList}>
                {results.rejected_alternatives.map((item) => (
                  <article key={item.recommendation_id}>
                    <strong>{item.name}</strong>
                  </article>
                ))}
              </div>
            </div>
          ) : null}
        </section>
      </section>
    </main>
  )
}
