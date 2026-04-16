import Link from 'next/link'

import styles from './page.module.css'

export default function NotFound() {
  return (
    <main className={styles.page}>
      <section className={styles.shell}>
        <div className={styles.radarCard}>
          <p className={styles.kicker}>FINDEC-RS</p>
          <h1>Page Not Found</h1>
          <p className={styles.notFoundText}>Return to the dashboard to continue your financial fit brief.</p>
          <Link className={styles.primaryButton} href="/">
            Dashboard
          </Link>
        </div>
      </section>
    </main>
  )
}
