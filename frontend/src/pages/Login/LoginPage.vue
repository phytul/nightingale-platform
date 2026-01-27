<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";
import TerminalWindow from "@/components/TerminalWindow.vue";

// 模式切换：login 或 register
const mode = ref<"login" | "register">("login");

// 登录表单
const loginEmail = ref("");
const password = ref("");
const showPassword = ref(false);

// 注册表单
const email = ref("");
const verificationCode = ref("");
const registerPassword = ref("");
const confirmPassword = ref("");
const showRegisterPassword = ref(false);
const showConfirmPassword = ref(false);
const codeCountdown = ref(0);
const isSendingCode = ref(false);

// 验证码倒计时
let countdownTimer: number | null = null;

const startCountdown = () => {
  codeCountdown.value = 60;
  countdownTimer = window.setInterval(() => {
    codeCountdown.value--;
    if (codeCountdown.value <= 0) {
      if (countdownTimer) {
        clearInterval(countdownTimer);
        countdownTimer = null;
      }
    }
  }, 1000);
};

const sendVerificationCode = async () => {
  if (!email.value || !isValidEmail(email.value)) {
    console.error("请输入有效的邮箱地址");
    return;
  }

  if (codeCountdown.value > 0) return;

  isSendingCode.value = true;
  try {
    // TODO: 调用发送验证码API
    console.log("发送验证码到:", email.value);
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));
    startCountdown();
  } catch (error) {
    console.error("发送验证码失败:", error);
  } finally {
    isSendingCode.value = false;
  }
};

const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const isPasswordMatch = computed(() => {
  if (!registerPassword.value || !confirmPassword.value) return true;
  return registerPassword.value === confirmPassword.value;
});

const handleLogin = () => {
  // 登录逻辑
  console.log("登录", { email: loginEmail.value, password: password.value });
};

const handleRegister = () => {
  if (!isPasswordMatch.value) {
    console.error("两次输入的密码不一致");
    return;
  }
  if (!verificationCode.value) {
    console.error("请输入验证码");
    return;
  }
  // 注册逻辑
  console.log("注册", {
    email: email.value,
    verificationCode: verificationCode.value,
    password: registerPassword.value,
  });
};

// 清理定时器
const cleanup = () => {
  if (countdownTimer) {
    clearInterval(countdownTimer);
    countdownTimer = null;
  }
};

// 组件卸载时清理
onUnmounted(() => {
  cleanup();
});
</script>

<template>
  <div class="login-container">
    <TerminalWindow :title="mode === 'login' ? 'login@nightingale:~' : 'register@nightingale:~'">
      <div class="terminal-output">
        <div class="command-line">
          <span class="prompt">$</span>
          <span class="command">cat /etc/motd</span>
        </div>
        <div class="output-text">
          <div class="welcome-banner">
            <span class="bracket">[</span> Nightingale Platform <span class="bracket">]</span>
          </div>
          <div class="info-line">
            <span class="symbol">></span>
            {{ mode === "login" ? "Authentication Required" : "Registration Required" }}
          </div>
        </div>
      </div>

      <!-- 模式切换 -->
      <div class="mode-switch">
        <button
          :class="['mode-button', { active: mode === 'login' }]"
          @click="mode = 'login'"
        >
          <span class="prompt">$</span>
          <span class="command-text">login</span>
        </button>
        <span class="mode-separator">|</span>
        <button
          :class="['mode-button', { active: mode === 'register' }]"
          @click="mode = 'register'"
        >
          <span class="prompt">$</span>
          <span class="command-text">register</span>
        </button>
      </div>

      <!-- 登录表单 -->
      <div v-if="mode === 'login'" class="form-card">
        <v-form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="loginEmail"
              placeholder="email"
              type="email"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
              autocomplete="email"
            ></v-text-field>
          </div>

          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="password"
              variant="plain"
              density="compact"
              class="terminal-input password-input"
              hide-details="auto"
              autocomplete="current-password"
              @click:append-inner="showPassword = !showPassword"
            >
              <template #append-inner>
                <v-icon
                  :icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  size="small"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                ></v-icon>
              </template>
            </v-text-field>
          </div>

          <div class="command-execute">
            <span class="prompt">$</span>
            <v-btn type="submit" variant="text" class="execute-button" size="small">
              <span class="command-text">./login.sh</span>
              <span class="cursor-blink">_</span>
            </v-btn>
          </div>
        </v-form>
      </div>

      <!-- 注册表单 -->
      <div v-if="mode === 'register'" class="form-card">
        <v-form @submit.prevent="handleRegister" class="register-form">
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="email"
              placeholder="email"
              type="email"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
              autocomplete="email"
            ></v-text-field>
          </div>

          <div class="input-group verification-code-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="verificationCode"
              placeholder="verification code"
              variant="plain"
              density="compact"
              class="terminal-input code-input"
              hide-details="auto"
              autocomplete="off"
            ></v-text-field>
            <v-btn
              :disabled="codeCountdown > 0 || isSendingCode || !isValidEmail(email)"
              variant="text"
              class="send-code-button"
              size="small"
              @click="sendVerificationCode"
            >
              <span v-if="codeCountdown > 0" class="countdown-text">{{ codeCountdown }}s</span>
              <span v-else class="send-text">发送</span>
            </v-btn>
          </div>

          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="registerPassword"
              :type="showRegisterPassword ? 'text' : 'password'"
              placeholder="password"
              variant="plain"
              density="compact"
              class="terminal-input password-input"
              hide-details="auto"
              autocomplete="new-password"
              @click:append-inner="showRegisterPassword = !showRegisterPassword"
            >
              <template #append-inner>
                <v-icon
                  :icon="showRegisterPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  size="small"
                  class="password-toggle"
                  @click="showRegisterPassword = !showRegisterPassword"
                ></v-icon>
              </template>
            </v-text-field>
          </div>

          <div class="input-group" :class="{ 'password-mismatch': !isPasswordMatch }">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="confirm password"
              variant="plain"
              density="compact"
              class="terminal-input password-input"
              hide-details="auto"
              autocomplete="new-password"
              @click:append-inner="showConfirmPassword = !showConfirmPassword"
            >
              <template #append-inner>
                <v-icon
                  :icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  size="small"
                  class="password-toggle"
                  @click="showConfirmPassword = !showConfirmPassword"
                ></v-icon>
              </template>
            </v-text-field>
          </div>

          <div v-if="!isPasswordMatch && confirmPassword" class="error-message">
            <span class="error-symbol">!</span>
            <span>密码不一致</span>
          </div>

          <div class="command-execute">
            <span class="prompt">$</span>
            <v-btn
              type="submit"
              variant="text"
              class="execute-button"
              size="small"
              :disabled="!isPasswordMatch"
            >
              <span class="command-text">./register.sh</span>
              <span class="cursor-blink">_</span>
            </v-btn>
          </div>
        </v-form>
      </div>
    </TerminalWindow>
  </div>
</template>

<style scoped lang="scss">
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
  padding: calc($space * 8);
}

.terminal-output {
  padding-bottom: calc($space * 6);
  border-bottom: 1px dashed $form-card-border-mix-result;
  padding-left: 0;
  padding-right: 0;
}

.command-line {
  display: flex;
  align-items: center;
  gap: calc($space * 2);
  margin-bottom: calc($space * 4);
  font-size: 0.875rem;
}

.prompt {
  color: $green-500;
  font-weight: 600;
  font-family: $font-mono;
}

.command {
  color: $foreground;
  font-family: $font-mono;
}

.output-text {
  padding-left: calc($space * 6);
  font-size: 0.875rem;
  line-height: 1.6;
}

.welcome-banner {
  margin-bottom: calc($space * 4);
  color: $foreground;
  font-weight: 500;

  .bracket {
    color: $green-500;
    font-weight: 600;
  }
}

.info-line {
  color: $muted-foreground;
  font-family: $font-mono;

  .symbol {
    color: $green-500;
    margin-right: calc($space * 2);
  }
}

.form-card {
  margin-left: 0;
  margin-right: 0;
  padding: calc($space * 8) calc($space * 10);
  background-color: color-mix(in srgb, $background 100%, $form-card-bg-mix);
  border: 1px solid color-mix(in srgb, $border-color 20%, $form-card-border-mix);
  border-radius: 4px;
  box-shadow:
    inset 0 1px 2px color-mix(in srgb, $form-card-shadow 5%, transparent),
    inset 0 -1px 2px color-mix(in srgb, $form-card-shadow 2%, transparent),
    0 1px 1px color-mix(in srgb, $form-card-shadow 2%, transparent);
}

.login-form {
  margin: 0;
}

.input-group {
  display: flex;
  align-items: center;
  gap: calc($space * 3);
  margin-bottom: calc($space * 6);
  padding: calc($space * 2) 0;
  position: relative;
  transition: all 0.2s ease;
  border-bottom: 1px solid color-mix(in srgb, $border-color 30%, transparent);

  &:hover {
    .input-prompt {
      opacity: 1;
      transform: scale(1.1);
    }

    .password-toggle {
      opacity: 1;
      visibility: visible;
    }

    border-bottom-color: $form-card-border-mix-result;
  }

  &:has(.terminal-input:focus) {
    .input-prompt {
      opacity: 1;
      color: $green-500;
      animation: pulse 1.5s ease-in-out infinite;
    }

    .password-toggle {
      opacity: 1;
      visibility: visible;
    }

    border-bottom-color: $green-500;
    border-bottom-width: 2px;
  }
}

.input-prompt {
  color: $green-500;
  font-weight: 600;
  font-size: 0.875rem;
  font-family: $font-mono;
  min-width: 12px;
  transition: all 0.2s ease;
  opacity: 0.7;
  cursor: default;
}

.terminal-input {
  flex: 1;
  font-family: $font-mono;
  font-size: 0.875rem;
  position: relative;
  transition: all 0.2s ease;

  :deep(.v-field) {
    background-color: transparent;
    box-shadow: none;
    transition: all 0.2s ease;
  }

  :deep(.v-field__input) {
    min-height: 32px;
    padding: 4px 0;
    color: $foreground;
    font-family: $font-mono;
    transition: all 0.2s ease;
    border-bottom: none;
  }

  :deep(.v-field__input::placeholder) {
    color: $muted-foreground;
    opacity: 0.5;
    transition: opacity 0.2s ease;
  }

  :deep(.v-field__outline) {
    display: none;
  }

  :deep(.v-field__input:focus) {
    outline: none;
  }

  &:hover {
    :deep(.v-field__input::placeholder) {
      opacity: 0.8;
    }
  }

  &:has(.v-field__input:focus) {
    :deep(.v-field__input::placeholder) {
      opacity: 0.3;
    }
  }
}

.password-input {
  :deep(.v-field__input) {
    letter-spacing: 2px;
  }
}

.password-toggle {
  color: $muted-foreground;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 4px;
  border-radius: 4px;
  opacity: 0;
  visibility: hidden;

  &:hover {
    color: $green-500;
    background-color: color-mix(in oklab, $green-500 10%, transparent);
    transform: scale(1.1);
  }

  &:active {
    transform: scale(0.95);
  }
}

.command-execute {
  display: flex;
  align-items: center;
  gap: calc($space * 3);
  padding-top: calc($space * 6);
}

.execute-button {
  padding: calc($space * 3) calc($space * 6);
  text-transform: none;
  font-family: $font-mono;
  font-size: 0.875rem;
  color: $foreground;
  min-width: auto;
  height: auto;
  border-radius: 4px;
  transition: all 0.2s ease;
  cursor: pointer;
  position: relative;
  border: 1px solid transparent;
  animation: button-pulse 2s ease-in-out infinite;

  &::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 4px;
    padding: 1px;
    background: conic-gradient(
      from 0deg,
      color-mix(in oklab, $green-500 30%, transparent) 0deg,
      color-mix(in oklab, $green-500 50%, transparent) 60deg,
      $green-500 120deg,
      color-mix(in oklab, $green-500 50%, transparent) 180deg,
      color-mix(in oklab, $green-500 30%, transparent) 240deg,
      color-mix(in oklab, $green-500 30%, transparent) 360deg
    );
    -webkit-mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    mask-composite: exclude;
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &:hover {
    background-color: color-mix(in oklab, $green-500 15%, transparent);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px color-mix(in oklab, $green-500 20%, transparent);
    animation: none;

    &::before {
      opacity: 1;
      animation: border-gradient-flow 3s linear infinite;
    }

    .command-text {
      color: $green-500;
    }
  }

  &:active {
    transform: translateY(0);
    background-color: color-mix(in oklab, $green-500 20%, transparent);
    animation: none;
  }

  .command-text {
    color: $foreground;
    transition: color 0.2s ease;
    position: relative;
    z-index: 1;
  }

  .cursor-blink {
    color: $green-500;
    animation: blink 1s infinite;
    margin-left: 2px;
    position: relative;
    z-index: 1;
  }
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes button-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 color-mix(in oklab, $green-500 0%, transparent);
  }
  50% {
    box-shadow: 0 0 0 4px color-mix(in oklab, $green-500 15%, transparent);
  }
}

// 模式切换
.mode-switch {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: calc($space * 4);
  padding: calc($space * 6) 0;
  margin-bottom: calc($space * 4);
  border-bottom: 1px dashed $form-card-border-mix-result;
}

.mode-button {
  display: flex;
  align-items: center;
  gap: calc($space * 2);
  padding: calc($space * 2) calc($space * 4);
  background: transparent;
  border: none;
  cursor: pointer;
  font-family: $font-mono;
  font-size: 0.875rem;
  color: $muted-foreground;
  transition: all 0.2s ease;
  border-radius: 4px;

  .prompt {
    color: $muted-foreground;
    transition: color 0.2s ease;
  }

  .command-text {
    color: $muted-foreground;
    transition: color 0.2s ease;
  }

  &:hover {
    background-color: color-mix(in oklab, $green-500 10%, transparent);
    color: $foreground;

    .prompt {
      color: $green-500;
    }

    .command-text {
      color: $foreground;
    }
  }

  &.active {
    color: $foreground;

    .prompt {
      color: $green-500;
      animation: pulse 1.5s ease-in-out infinite;
    }

    .command-text {
      color: $foreground;
    }
  }
}

.mode-separator {
  color: $muted-foreground;
  font-family: $font-mono;
  opacity: 0.5;
}

// 验证码输入组
.verification-code-group {
  position: relative;
  padding-right: 80px;
}

.code-input {
  flex: 1;
}

.send-code-button {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  padding: calc($space * 2) calc($space * 4);
  min-width: auto;
  height: auto;
  font-family: $font-mono;
  font-size: 0.75rem;
  color: $green-500;
  text-transform: none;
  border-radius: 4px;
  transition: all 0.2s ease;
  border: 1px solid transparent;

  &:hover:not(:disabled) {
    background-color: color-mix(in oklab, $green-500 15%, transparent);
    border-color: color-mix(in oklab, $green-500 30%, transparent);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .countdown-text {
    color: $muted-foreground;
    font-family: $font-mono;
  }

  .send-text {
    color: $green-500;
    font-family: $font-mono;
  }
}

// 密码不匹配样式
.input-group.password-mismatch {
  border-bottom-color: #ff5f57;

  .input-prompt {
    color: #ff5f57;
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: calc($space * 2);
  padding: calc($space * 3) calc($space * 4);
  margin-top: calc($space * 2);
  margin-bottom: calc($space * 4);
  background-color: color-mix(in oklab, #ff5f57 10%, transparent);
  border: 1px solid color-mix(in oklab, #ff5f57 30%, transparent);
  border-radius: 4px;
  color: #ff5f57;
  font-family: $font-mono;
  font-size: 0.75rem;

  .error-symbol {
    color: #ff5f57;
    font-weight: 600;
  }
}

.execute-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  animation: none;

  &:hover {
    background-color: transparent;
    transform: none;
    box-shadow: none;

    &::before {
      opacity: 0;
    }

    .command-text {
      color: $foreground;
    }
  }
}
</style>
