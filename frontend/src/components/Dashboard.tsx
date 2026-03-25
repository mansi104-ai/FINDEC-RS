import React from 'react'
import RecommendationFeed from './RecommendationFeed'
import BiasProfileChart from './BiasProfileChart'

export default function Dashboard() {
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <BiasProfileChart />
      <RecommendationFeed />
    </div>
  )
}
