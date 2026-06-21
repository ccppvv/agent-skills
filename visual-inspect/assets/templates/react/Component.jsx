import styles from './Component.module.css';

export function Component({ title, children, variant = 'default' }) {
  return (
    <div className={`${styles.container} ${styles[variant]}`}>
      <h2 className={styles.title}>{title}</h2>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
}
