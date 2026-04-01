import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getRecommendations = async (userId: string) => {
  const response = await apiClient.get(`/recommendations/${userId}`)
  return response.data
}

export const getBiasProfile = async (userId: string) => {
  const response = await apiClient.get(`/bias-profile/${userId}`)
  return response.data
}

export const analyzeAsset = async (assetId: string) => {
  const response = await apiClient.post('/analyze', { assetId })
  return response.data
}

export type HoldingInput = {
  name: string
  sector: string
  value: number
}

export type SuitabilityRequest = {
  age: number
  income_level: string
  monthly_income: number
  monthly_expenses: number
  income_stability: string
  investment_experience: string
  financial_literacy_level: string
  current_holdings: HoldingInput[]
  current_holdings_value: number
  liabilities: number
  emergency_fund_months: number
  financial_goal: string
  time_horizon_years: number
  liquidity_needs: string
  return_expectations: string
  volatility_comfort: number
  drawdown_tolerance: number
  return_preference: string
}

export type ScoredRecommendation = {
  recommendation_id: string
  name: string
  asset_type: string
  suitability_score: number
  suitability_label: string
  explanation_summary: string
  risk_warnings: string[]
  confidence_score: number
  content_match_score: number
  rationale_factors: string[]
  next_best_action: string
}

export type RejectedAlternative = {
  recommendation_id: string
  name: string
  reason: string
}

export type SuitabilityResponse = {
  normalized_user_profile: Record<string, unknown>
  goal_context: Record<string, unknown>
  risk_profile: Record<string, unknown>
  preference_profile: Record<string, unknown>
  recommendations: ScoredRecommendation[]
  rejected_alternatives: RejectedAlternative[]
  engine_summary: string
}

export const evaluateSuitability = async (payload: SuitabilityRequest) => {
  const response = await apiClient.post<SuitabilityResponse>('/api/recommendations/suitability', payload)
  return response.data
}

export default apiClient
