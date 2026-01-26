<script setup lang="ts">
import { ref } from "vue";
import TerminalWindow from "@/components/TerminalWindow.vue";

const username = ref("");
const password = ref("");
const showPassword = ref(false);

const handleLogin = () => {
  // 登录逻辑
  console.log("登录", { username: username.value, password: password.value });
};
</script>

<template>
  <div class="login-container">
    <TerminalWindow title="login@nightingale:~">
      <div class="terminal-output">
        <div class="command-line">
          <span class="prompt">$</span>
          <span class="command">cat /etc/motd</span>
        </div>
        <div class="output-text">
          <div class="welcome-banner">
            <span class="bracket">[</span> Nightingale Platform <span class="bracket">]</span>
          </div>
          <div class="info-line"><span class="symbol">></span> Authentication Required</div>
        </div>
      </div>

      <div class="form-card">
        <v-form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="username"
              placeholder="username"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
              autocomplete="username"
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
</style>
