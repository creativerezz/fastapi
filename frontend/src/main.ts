import './app.css';
import Test from './Test.svelte';
import { mount } from 'svelte';

const app = mount(Test, {
  target: document.getElementById('app')!,
});

export default app;
