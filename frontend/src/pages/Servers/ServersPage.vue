<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from "vue";
import TerminalWindow from "@/components/TerminalWindow.vue";

// 认证方式
type AuthMethod = "password" | "key";

// 服务器配置（当前仅支持一台）
const serverConfig = ref({
  name: "默认服务器",
  host: "",
  port: 22,
  username: "",
  authMethod: "password" as AuthMethod,
  password: "",
  privateKeyPath: "~/.ssh/id_rsa",
});

const showPassword = ref(false);
const isSaving = ref(false);
const saveSuccess = ref(false);

// 终端连接状态
const isConnected = ref(false);
const isConnecting = ref(false);
const terminalLines = ref<{ type: "input" | "output" | "error"; text: string }[]>([]);
const commandInput = ref("");
const terminalContainer = ref<HTMLElement | null>(null);

const configStorageKey = "nightingale_server_config";

// 从本地存储加载配置
onMounted(() => {
  try {
    const raw = localStorage.getItem(configStorageKey);
    if (raw) {
      const parsed = JSON.parse(raw);
      serverConfig.value = { ...serverConfig.value, ...parsed };
    }
  } catch {
    // 忽略无效存储
  }
});

const canSave = computed(() => {
  return serverConfig.value.host.trim() !== "" && serverConfig.value.username.trim() !== "";
});

const canConnect = computed(() => {
  if (serverConfig.value.authMethod === "password") {
    return canSave.value && serverConfig.value.password !== "";
  }
  return canSave.value && serverConfig.value.privateKeyPath.trim() !== "";
});

const saveConfig = async () => {
  if (!canSave.value) return;
  isSaving.value = true;
  saveSuccess.value = false;
  try {
    await new Promise((r) => setTimeout(r, 400));
    const toStore = {
      name: serverConfig.value.name,
      host: serverConfig.value.host,
      port: serverConfig.value.port,
      username: serverConfig.value.username,
      authMethod: serverConfig.value.authMethod,
      privateKeyPath: serverConfig.value.privateKeyPath,
    };
    if (serverConfig.value.authMethod === "password") {
      (toStore as Record<string, unknown>)["password"] = serverConfig.value.password;
    }
    localStorage.setItem(configStorageKey, JSON.stringify(toStore));
    saveSuccess.value = true;
    setTimeout(() => (saveSuccess.value = false), 2000);
  } finally {
    isSaving.value = false;
  }
};

// 连接服务器（当前为前端模拟，后续可对接 WebSocket/SSH 代理）
const connect = async () => {
  if (!canConnect.value || isConnecting.value) return;
  isConnecting.value = true;
  terminalLines.value = [];
  try {
    await new Promise((r) => setTimeout(r, 800));
    isConnected.value = true;
    appendOutput(
      `Connected to ${serverConfig.value.username}@${serverConfig.value.host}:${serverConfig.value.port}.`,
    );
    appendOutput("Nightingale 调试终端（当前为模拟会话，实际执行需后端 SSH/WebSocket 支持）");
    appendOutput("");
  } finally {
    isConnecting.value = false;
  }
};

const disconnect = () => {
  isConnected.value = false;
  terminalLines.value = [];
  commandInput.value = "";
};

function appendOutput(text: string, isError = false) {
  terminalLines.value.push({
    type: isError ? "error" : "output",
    text,
  });
  nextTick(() => {
    terminalContainer.value?.scrollTo({ top: terminalContainer.value.scrollHeight, behavior: "smooth" });
  });
}

function appendInput(line: string) {
  terminalLines.value.push({ type: "input", text: line });
}

// 简单模拟命令执行（便于调试 UI，实际应由后端返回）
const mockExecute = (cmd: string): string => {
  const c = cmd.trim().toLowerCase();
  if (!c) return "";
  if (c === "help") {
    return "可用命令: help, whoami, hostname, pwd, echo, exit. 当前为前端模拟。";
  }
  if (c === "whoami") return serverConfig.value.username;
  if (c === "hostname") return serverConfig.value.host || "localhost";
  if (c === "pwd") return "/home/" + serverConfig.value.username;
  if (c.startsWith("echo ")) return cmd.slice(5).trim();
  if (c === "exit" || c === "quit") {
    disconnect();
    return "Connection closed.";
  }
  return `bash: ${cmd.split(/\s/)[0]}: command not found`;
};

const executeCommand = () => {
  const line = commandInput.value.trim();
  if (!line && !isConnected.value) return;
  if (!isConnected.value) return;

  appendInput(`$ ${line}`);
  commandInput.value = "";

  const result = mockExecute(line);
  if (result) appendOutput(result, result.includes("command not found") || result.includes("error"));
  if (line.toLowerCase() === "exit" || line.toLowerCase() === "quit") return;

  nextTick(() => {
    terminalContainer.value?.scrollTo({ top: terminalContainer.value.scrollHeight, behavior: "smooth" });
  });
};
</script>

<template>
  <div class="servers-page">
    <div class="page-header">
      <div class="command-line">
        <span class="prompt">$</span>
        <span class="command">cat servers/README.md</span>
      </div>
      <div class="output-text">
        <div class="info-line">
          <span class="symbol">></span>
          服务器管理：配置一台服务器并接入其命令行进行简单调试。
        </div>
      </div>
    </div>

    <div class="panels">
      <!-- 服务器配置 -->
      <TerminalWindow title="server-config@nightingale:~" max-width="100%" class="config-panel">
        <div class="terminal-output">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">./edit-server.sh</span>
          </div>
          <div class="output-text">
            <span class="symbol">></span>
            编辑服务器连接信息（当前仅支持一台）
          </div>
        </div>

        <div class="form-card">
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="serverConfig.name"
              placeholder="连接名称"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
            />
          </div>
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="serverConfig.host"
              placeholder="主机 (host / IP)"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
            />
          </div>
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model.number="serverConfig.port"
              placeholder="端口"
              type="number"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
            />
          </div>
          <div class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="serverConfig.username"
              placeholder="用户名"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
            />
          </div>

          <div class="auth-method">
            <span class="input-prompt">$</span>
            <div class="method-options">
              <button
                :class="['mode-button', { active: serverConfig.authMethod === 'password' }]"
                @click="serverConfig.authMethod = 'password'"
              >
                password
              </button>
              <span class="mode-separator">|</span>
              <button
                :class="['mode-button', { active: serverConfig.authMethod === 'key' }]"
                @click="serverConfig.authMethod = 'key'"
              >
                key
              </button>
            </div>
          </div>

          <div v-if="serverConfig.authMethod === 'password'" class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="serverConfig.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="密码"
              variant="plain"
              density="compact"
              class="terminal-input password-input"
              hide-details="auto"
              @click:append-inner="showPassword = !showPassword"
            >
              <template #append-inner>
                <v-icon
                  :icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  size="small"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                />
              </template>
            </v-text-field>
          </div>
          <div v-else class="input-group">
            <span class="input-prompt">$</span>
            <v-text-field
              v-model="serverConfig.privateKeyPath"
              placeholder="私钥路径 (e.g. ~/.ssh/id_rsa)"
              variant="plain"
              density="compact"
              class="terminal-input"
              hide-details="auto"
            />
          </div>

          <div class="actions">
            <span class="prompt">$</span>
            <v-btn
              :disabled="!canSave || isSaving"
              variant="text"
              class="execute-button"
              size="small"
              @click="saveConfig"
            >
              <span class="command-text">{{ isSaving ? "保存中…" : "保存配置" }}</span>
              <span v-if="saveSuccess" class="ok-tag"> OK</span>
            </v-btn>
            <template v-if="!isConnected">
              <v-btn
                :disabled="!canConnect || isConnecting"
                variant="text"
                class="execute-button connect-btn"
                size="small"
                @click="connect"
              >
                <span class="command-text">{{ isConnecting ? "连接中…" : "连接终端" }}</span>
              </v-btn>
            </template>
            <template v-else>
              <v-btn variant="text" class="execute-button disconnect-btn" size="small" @click="disconnect">
                <span class="command-text">断开连接</span>
              </v-btn>
            </template>
          </div>
        </div>
      </TerminalWindow>

      <!-- 命令行终端 -->
      <TerminalWindow
        :title="
          isConnected
            ? `${serverConfig.username}@${serverConfig.host}:~`
            : 'terminal@nightingale:~'
        "
        max-width="100%"
        class="terminal-panel"
      >
        <div v-if="!isConnected" class="terminal-output">
          <div class="command-line">
            <span class="prompt">$</span>
            <span class="command">ssh {{ serverConfig.username || "user" }}@{{ serverConfig.host || "host" }}</span>
          </div>
          <div class="output-text">
            <span class="symbol">></span>
            请先保存配置并点击「连接终端」，再在此处输入命令进行简单调试。
          </div>
        </div>

        <div v-else class="shell-area">
          <div ref="terminalContainer" class="terminal-output-scroll">
            <div
              v-for="(line, i) in terminalLines"
              :key="i"
              :class="['terminal-line', line.type]"
            >
              <span v-if="line.type === 'input'" class="line-prompt">$</span>
              <span class="line-text">{{ line.text }}</span>
            </div>
            <div class="terminal-line input-line">
              <span class="line-prompt">$</span>
              <input
                v-model="commandInput"
                type="text"
                class="shell-input"
                placeholder="输入命令…"
                autocomplete="off"
                @keydown.enter="executeCommand"
              />
              <span class="cursor-blink">_</span>
            </div>
          </div>
        </div>
      </TerminalWindow>
    </div>
  </div>
</template>

<style scoped lang="scss">
.servers-page {
  padding: calc($space * 8) calc($space * 10);
  max-width: $container-7xl;
  margin: 0 auto;
}

.page-header {
  margin-bottom: calc($space * 10);

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
    color: $muted-foreground;
    font-family: $font-mono;

    .symbol {
      color: $green-500;
      margin-right: calc($space * 2);
    }
  }
}

.panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: calc($space * 10);
  align-items: start;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.config-panel,
.terminal-panel {
  min-width: 0;
}

.terminal-output {
  padding-bottom: calc($space * 6);
  border-bottom: 1px dashed $form-card-border-mix-result;
  margin-bottom: calc($space * 6);
}

.form-card {
  padding: 0;
  background: transparent;
  border: none;
  box-shadow: none;
}

.input-group {
  display: flex;
  align-items: center;
  gap: calc($space * 3);
  margin-bottom: calc($space * 6);
  padding: calc($space * 2) 0;
  border-bottom: 1px solid color-mix(in srgb, $border-color 30%, transparent);
  transition: border-color 0.2s ease;

  &:hover {
    border-bottom-color: $form-card-border-mix-result;
  }

  &:has(.terminal-input:focus),
  &:has(.v-field--focused) {
    border-bottom-color: $green-500;
  }
}

.input-prompt {
  color: $green-500;
  font-weight: 600;
  font-size: 0.875rem;
  font-family: $font-mono;
  min-width: 12px;
}

.terminal-input {
  flex: 1;
  font-family: $font-mono;
  font-size: 0.875rem;

  :deep(.v-field) {
    background: transparent;
    box-shadow: none;
  }

  :deep(.v-field__input) {
    min-height: 32px;
    padding: 4px 0;
    color: $foreground;
    font-family: $font-mono;
  }

  :deep(.v-field__outline) {
    display: none;
  }
}

.password-toggle {
  color: $muted-foreground;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;

  &:hover {
    color: $green-500;
  }
}

.auth-method {
  display: flex;
  align-items: center;
  gap: calc($space * 3);
  margin-bottom: calc($space * 6);
  padding: calc($space * 2) 0;
}

.method-options {
  display: flex;
  align-items: center;
  gap: calc($space * 2);
}

.mode-button {
  padding: calc($space * 2) calc($space * 4);
  background: transparent;
  border: none;
  cursor: pointer;
  font-family: $font-mono;
  font-size: 0.875rem;
  color: $muted-foreground;
  border-radius: 4px;
  transition: all 0.2s ease;

  &:hover {
    background-color: color-mix(in oklab, $green-500 10%, transparent);
    color: $foreground;
  }

  &.active {
    color: $green-500;
  }
}

.mode-separator {
  color: $muted-foreground;
  opacity: 0.5;
}

.actions {
  display: flex;
  align-items: center;
  gap: calc($space * 4);
  flex-wrap: wrap;
  padding-top: calc($space * 6);

  .prompt {
    color: $green-500;
    font-weight: 600;
    font-family: $font-mono;
  }
}

.execute-button {
  text-transform: none;
  font-family: $font-mono;
  font-size: 0.875rem;
  color: $foreground;
  min-width: auto;

  .command-text {
    color: inherit;
  }

  .ok-tag {
    color: $green-500;
    margin-left: calc($space * 2);
  }

  &:hover:not(:disabled) {
    background-color: color-mix(in oklab, $green-500 15%, transparent);
  }

  &.connect-btn:hover:not(:disabled) .command-text {
    color: $green-500;
  }

  &.disconnect-btn:hover .command-text {
    color: #ff5f57;
  }
}

.shell-area {
  min-height: 280px;
  display: flex;
  flex-direction: column;
}

.terminal-output-scroll {
  flex: 1;
  max-height: 360px;
  overflow-y: auto;
  padding-right: calc($space * 4);
}

.terminal-line {
  font-family: $font-mono;
  font-size: 0.875rem;
  margin-bottom: calc($space * 2);
  display: flex;
  align-items: center;
  gap: calc($space * 2);
  word-break: break-all;

  .line-prompt {
    color: $green-500;
    font-weight: 600;
    flex-shrink: 0;
  }

  .line-text {
    color: $foreground;
  }

  &.error .line-text {
    color: #ff5f57;
  }

  &.input-line {
    margin-bottom: 0;
  }
}

.shell-input {
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  outline: none;
  color: $foreground;
  font-family: $font-mono;
  font-size: 0.875rem;

  &::placeholder {
    color: $muted-foreground;
    opacity: 0.6;
  }
}

.cursor-blink {
  color: $green-500;
  animation: blink 1s infinite;
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
</style>
