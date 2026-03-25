export interface BiasMetrics {
  biasScore: number
  riskLevel: 'low' | 'medium' | 'high'
  factors: string[]
}

export const calculateBiasScore = (factors: string[]): number => {
  return Math.min(100, factors.length * 10)
}

export const getRiskLevel = (score: number): 'low' | 'medium' | 'high' => {
  if (score < 30) return 'low'
  if (score < 70) return 'medium'
  return 'high'
}

export const formatBiasReport = (metrics: BiasMetrics): string => {
  return `Bias Score: ${metrics.biasScore}/100 - Risk Level: ${metrics.riskLevel}`
}
