<script setup lang="ts">
</script>

<template>
  <div class="bg-white">

    <!-- HERO -->
    <section class="py-24 bg-gradient-to-br from-secondary to-black text-white text-center">
      <div class="max-w-4xl mx-auto px-6" data-aos="fade-up">

        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          Services That Build
          <span class="text-primary">Real Products</span>
        </h1>

        <p class="text-gray-300 text-lg mb-6">
          We don’t just design — we engineer scalable digital systems for modern businesses.
        </p>

        <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl shadow-lg hover:scale-105 transition"
        >
          Start Your Project
        </button>

      </div>
    </section>

    <!-- SERVICES -->
    <section class="py-20">
      <div class="max-w-7xl mx-auto px-6">

        <h2 class="text-3xl font-bold text-center mb-12" data-aos="fade-up">
          What We Offer
        </h2>

        <div class="grid md:grid-cols-3 gap-8">

          <!-- SERVICE 1 -->
          <div data-aos="zoom-in"
            class="p-6 bg-gray-50 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-2 transition">

            <img src="https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg"
                 class="rounded-lg mb-4 h-40 w-full object-cover"/>

            <h3 class="text-xl font-semibold mb-2">Web Development</h3>

            <p class="text-gray-600 text-sm mb-4">
              High-performance websites built for speed, SEO, and conversion.
            </p>

            <ul class="text-sm text-gray-500 space-y-1">
              <li>• Responsive design</li>
              <li>• SEO optimization</li>
              <li>• Fast loading speeds</li>
            </ul>

          </div>

          <!-- SERVICE 2 -->
          <div data-aos="zoom-in" data-aos-delay="100"
            class="p-6 bg-gray-50 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-2 transition">

            <img src="https://images.pexels.com/photos/3861958/pexels-photo-3861958.jpeg"
                 class="rounded-lg mb-4 h-40 w-full object-cover"/>

            <h3 class="text-xl font-semibold mb-2">SaaS Systems</h3>

            <p class="text-gray-600 text-sm mb-4">
              Scalable dashboards and platforms tailored to your business logic.
            </p>

            <ul class="text-sm text-gray-500 space-y-1">
              <li>• Admin dashboards</li>
              <li>• Role-based systems</li>
              <li>• Analytics integration</li>
            </ul>

          </div>

          <!-- SERVICE 3 -->
          <div data-aos="zoom-in" data-aos-delay="200"
            class="p-6 bg-gray-50 rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-2 transition">

            <img src="https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg"
                 class="rounded-lg mb-4 h-40 w-full object-cover"/>

            <h3 class="text-xl font-semibold mb-2">Custom CMS</h3>

            <p class="text-gray-600 text-sm mb-4">
              Powerful content management systems built specifically for your workflow.
            </p>

            <ul class="text-sm text-gray-500 space-y-1">
              <li>• Easy content control</li>
              <li>• Custom dashboards</li>
              <li>• Secure backend</li>
            </ul>

          </div>

        </div>

      </div>
    </section>

    <!-- PROCESS -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-5xl mx-auto px-6 text-center">

        <h2 class="text-3xl font-bold mb-10" data-aos="fade-up">
          How We Work
        </h2>

        <div class="grid md:grid-cols-4 gap-6 text-sm">

          <div data-aos="fade-up">
            <h3 class="font-semibold">1. Discovery</h3>
            <p class="text-gray-500">Understand your goals</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="100">
            <h3 class="font-semibold">2. Design</h3>
            <p class="text-gray-500">Craft user experience</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="200">
            <h3 class="font-semibold">3. Build</h3>
            <p class="text-gray-500">Develop your system</p>
          </div>

          <div data-aos="fade-up" data-aos-delay="300">
            <h3 class="font-semibold">4. Launch</h3>
            <p class="text-gray-500">Deploy & support</p>
          </div>

        </div>

      </div>
    </section>

    <!-- WHY CHOOSE US -->
    <section class="py-20">
      <div class="max-w-6xl mx-auto px-6">

        <h2 class="text-3xl font-bold text-center mb-12" data-aos="fade-up">
          Why Choose FixKraft
        </h2>

        <div class="grid md:grid-cols-3 gap-6 text-center">

          <div data-aos="fade-up" class="p-6">
            <h3 class="font-semibold mb-2">⚡ Fast Delivery</h3>
            <p class="text-gray-500 text-sm">
              We build efficiently without compromising quality.
            </p>
          </div>

          <div data-aos="fade-up" data-aos-delay="100" class="p-6">
            <h3 class="font-semibold mb-2">🧠 Smart Systems</h3>
            <p class="text-gray-500 text-sm">
              Built with scalability and performance in mind.
            </p>
          </div>

          <div data-aos="fade-up" data-aos-delay="200" class="p-6">
            <h3 class="font-semibold mb-2">🎯 Business Focused</h3>
            <p class="text-gray-500 text-sm">
              Everything is aligned with your business goals.
            </p>
          </div>

        </div>

      </div>
    </section>

    <!-- CTA -->
    <section class="py-24 bg-black text-white text-center">
      <div data-aos="zoom-in">

        <h2 class="text-3xl font-bold mb-4">
          Ready to build your system?
        </h2>

        <p class="text-gray-300 mb-6">
          Let’s turn your idea into a working product.
        </p>

        <button
          @click="$router.push('/contact')"
          class="bg-primary px-6 py-3 rounded-xl shadow-lg hover:scale-105 transition"
        >
          Start a Project
        </button>

      </div>
    </section>

  </div>
</template>