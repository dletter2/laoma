<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <div class="footer-copyright">© 2024 资源分享站 All Rights Reserved</div>
      <div class="footer-disclaimer">
        <h4>免责声明</h4>
        <p>一、本站所有资源均由网友上传和分享，本站仅提供信息存储服务。资源内容的真实性、合法性、准确性由上传者负责，本站不对其内容承担任何审查或保证义务。</p>
        <p>二、用户因下载或使用本站资源而遭受的任何直接或间接损失（包括但不限于数据丢失、财产损失、系统故障等），均由用户自行承担，本站不承担任何赔偿责任。</p>
        <p>三、本站尊重知识产权。如果您发现本站资源侵犯了您的合法权益（包括但不限于著作权、商标权、专利权等），请将侵权资源链接及相关权属证明发送至站长邮箱：<a href="mailto:ifnocat@gmail.com">ifnocat@gmail.com</a>，我们将在收到有效通知后及时删除涉嫌侵权的内容。</p>
        <p>四、本声明最终解释权归本站所有，如有更新恕不另行通知。</p>
      </div>
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
.footer-copyright {
  margin-bottom: 12px;
}
.footer-disclaimer {
  max-width: 720px;
  margin: 0 auto;
  text-align: left;
  font-size: 12px;
  color: #999;
  line-height: 1.8;
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 6px;
}
.footer-disclaimer h4 {
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
}
.footer-disclaimer p {
  margin-bottom: 4px;
}
.footer-disclaimer a {
  color: var(--primary);
  text-decoration: none;
}
.footer-disclaimer a:hover {
  text-decoration: underline;
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .app-footer { margin-top: 40px; padding: 16px 0; }
  .footer-disclaimer { font-size: 11px; padding: 10px 12px; }
}
</style>
