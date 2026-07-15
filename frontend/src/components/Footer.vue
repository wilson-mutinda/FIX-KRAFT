<template>
    <footer class="bg-secondary text-white mt-20">
        <div class="max-w-7xl mx-auto px-6 py-10 grid md:grid-cols-3 gap-8">

            <!-- BRAND -->
            <div class="flex flex-col gap-3">

                <!-- router-link for the logo -->
                 <router-link to="/" class="flex items-center gap-1">
                    <!-- LOGO CONTAINER -->
                    <div class="h-20 w-40 flex items-center justify-center overflow-hidden rounded-md">
                        <img 
                        :src="logoUrl" 
                        alt="Logo"
                        class="h-full w-full object-contain"
                        />
                    </div>

                    <!-- TEXT -->
                    <h2 class="text-lg font-bold text-primary whitespace-nowrap">
                        FixKraft Digital
                    </h2>
                 </router-link>

                <!-- TAGLINE -->
                 <p class="text-sm text-gray-300 max-w-xs">Building modern digital products & systems.</p>
            </div>

            <div class="">
                <h3 class="font-semibold mb-2">Links</h3>
                <ul class=" space-y-2 text-sm text-gray-300">
                    
                    <li class="hover:text-white cursor-pointer"><a href="/">Home</a></li>
                    <li class="hover:text-white cursor-pointer"><a href="/services">Services</a></li>
                    <li class="hover:text-white cursor-pointer"><a href="/projects">Projects</a></li>
                    <li class="hover:text-white cursor-pointer"><a href="/blog">Blog</a></li>
                    <li class="hover:text-white cursor-pointer"><a href="/contact">Contact</a></li>
                </ul>
            </div>

            <div>
                <h3 class="font-semibold mb-3">Contact</h3>

                <div class="space-y-3 text-sm text-gray-300">

                    <!-- Email -->
                    <div class="flex items-center gap-2 hover:text-white transition">
                    <!-- <span></span> -->
                    <Mail class="w-4 h-4" />
                    <a href="mailto:info@fixkraftdigital.co.ke">
                        {{ config.email }}
                    </a>
                    </div>

                    <!-- Phone -->
                    <div class="flex items-center gap-2 hover:text-white transition">
                    <Phone class="w-4 h-4" />
                    <a href="tel:+254748929891">
                        {{ config.phone }}
                    </a>
                    </div>

                    <!-- Location -->
                    <div class="flex items-center gap-2">
                    <MapPin class="w-4 h-4" />
                    <span>{{ config.location }}</span>
                    </div>

                    <!-- Socials -->
                    <div class="flex items-center gap-4 pt-2">

                    <a href="#" class="hover:text-white transition">
                        <Globe class="w-5 h-5" />
                    </a>
                    <a href="#" class="hover:text-white transition">
                        <Briefcase class="w-5 h-5" />
                    </a>
                    <a href="#" class="hover:text-white transition">
                        <Twitter class="w-5 h-5" />
                    </a>

                    </div>

                </div>
                </div>
        </div>

        <div class="text-center text-sm py-4 border-t border-white/10">
            © {{ currentYear }} FixKraft Digital. All rights reserved
        </div>
    </footer>
</template>

<script setup lang="ts">
import { useSiteConfig } from '@/stores/siteConfig';
import { useThemeStore } from '@/stores/theme';
import { Briefcase, Globe, Mail, MapPin, Phone, Twitter } from 'lucide-vue-next';
import { computed } from 'vue';

const currentYear = new Date().getFullYear()

const config = useSiteConfig()

const theme = useThemeStore()

// Use destructured values for better reactivity in template
const { navLinks, email, phone, location } = config;

const logoUrl = computed(() => {
    return theme.dark ? '/fix-kraft-logo-blue-bg.svg' : '/fix-kraft-logo-blue-bg.svg'
})
</script>