import React from 'react'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>FINDEC-RS</h1>
      </div>
      <ul className="navbar-menu">
        <li><a href="/">Dashboard</a></li>
        <li><a href="/recommendations">Recommendations</a></li>
        <li><a href="/bias-report">Bias Report</a></li>
        <li><a href="/kg-explorer">KG Explorer</a></li>
      </ul>
    </nav>
  )
}
