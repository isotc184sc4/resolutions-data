<template>
  <div class="site-brand-bar" aria-hidden="true"></div>
  <header id="nav-header" class="site-header">
    <div class="site-header__inner">
      <a href="/" class="site-header__logo">
        <img src="/assets/iso-red.svg" alt="ISO" class="dark:hidden">
        <img src="/assets/iso-red.svg" alt="ISO" class="hidden dark:block">
        <span class="site-header__logo-text">ISO/TC 184/SC 4</span>
      </a>
      <div class="site-header__actions">
        <!-- Theme Toggle -->
        <button @click="toggleTheme" type="button" class="site-header__icon-btn" aria-label="Toggle dark mode">
          <svg v-if="!isDark" style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else style="width: 20px; height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>
      </div>
    </div>
  </header>

  <main>
    <router-view />
  </main>

  <footer class="site-footer">
    <div class="site-footer__inner">
      <div class="site-footer__grid" style="display: flex; justify-content: space-between;">
        <div class="site-footer__brand">
          <a href="/" class="site-footer__logo">
            <img src="/assets/iso-red.svg" alt="ISO" class="dark:hidden">
            <img src="/assets/iso-red.svg" alt="ISO" class="hidden dark:block">
            <span class="site-footer__logo-text">ISO/TC 184/SC 4</span>
          </a>
          <p class="site-footer__tagline">Industrial data</p>
        </div>
        <div>
          <h4 class="site-footer__heading">Links</h4>
          <ul class="site-footer__links">
            <li><a href="https://www.iso.org" class="site-footer__link">ISO.org</a></li>
            <li><a href="https://github.com/ISO-TC184-SC4" class="site-footer__link">GitHub</a></li>
          </ul>
        </div>
      </div>
      <div class="site-footer__bottom">
        <p class="site-footer__copy">
          &copy; {{ new Date().getFullYear() }} ISO/TC&nbsp;184/SC&nbsp;4
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDark = ref(false)

onMounted(() => {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true
  }
  if (document.documentElement.classList.contains('dark')) {
    isDark.value = true
  }
})

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}
</script>
