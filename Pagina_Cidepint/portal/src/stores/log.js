import { piniaInstance } from "../main";

export const useStore = piniaInstance.useStore();

export const state = () => ({
  isLogged: false,
});