import { useTheme } from "vuetify";

type CustomTheme = "customLightTheme" | "customDarkTheme";

/**
 * 自定义主题切换 hook
 */
const useCustomTheme = () => {
  const theme = useTheme();

  class ThemeController {
    currentTheme: CustomTheme = theme.global.name.value as CustomTheme;

    constructor() {
      this.currentTheme = theme.global.name.value as CustomTheme;
    }

    toggle() {
      const lightTheme: CustomTheme = "customLightTheme";
      const nextTheme: CustomTheme =
        this.currentTheme === lightTheme ? "customDarkTheme" : "customLightTheme";
      this.currentTheme = nextTheme;
      theme.change(nextTheme);
    }
  }

  return new ThemeController();
};

export default useCustomTheme;
