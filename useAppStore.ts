import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AppStore {
  darkMode: boolean;
  toggleDark: () => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      darkMode: false,
      toggleDark: () => set((s) => ({ darkMode: !s.darkMode })),
    }),
    { name: 'plantguard-settings' }
  )
);
