<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <span>© 2024 资源分享站 All Rights Reserved</span>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--bg-white);
  border-top: 1px solid var(--border-color);
  padding: 20px 0;
  margin-top: 60px;
}
.footer-inner {
  text-align: center;
  color: var(--text-secondary);
  font-size: 13px;
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .app-footer { margin-top: 40px; padding: 16px 0; }
  .footer-inner { font-size: 12px; }
}
</style>
