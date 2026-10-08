/** @type {const} */
const themeColors = {
  primary: { light: '#2563EB', dark: '#3B82F6' },
  background: { light: '#F8FAFC', dark: '#0F172A' },
  surface: { light: '#FFFFFF', dark: '#1E293B' },
  foreground: { light: '#0F172A', dark: '#F1F5F9' },
  muted: { light: '#64748B', dark: '#94A3B8' },
  border: { light: '#E2E8F0', dark: '#334155' },
  success: { light: '#16A34A', dark: '#4ADE80' },
  warning: { light: '#D97706', dark: '#FBBF24' },
  error: { light: '#DC2626', dark: '#F87171' },
  accent: { light: '#7C3AED', dark: '#A78BFA' },
  // 동그래 헤드셋의 주황색: "지금 눌러야 할 것"(시작·복습 버튼, 연속 학습 등)에만 쓴다
  highlight: { light: '#F0562E', dark: '#FF7A50' },
};

module.exports = { themeColors };
