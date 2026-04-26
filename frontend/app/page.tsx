"use client";

import { useRouter } from "next/navigation";
import { Heart, Sparkles, ArrowRight, Users, Zap, Star } from "lucide-react";
import { motion } from "motion/react";

export default function Home() {
  const router = useRouter();

  return (
    <div className="min-h-screen relative overflow-hidden" style={{ backgroundColor: '#f5f1ed' }}>

      {/* Subtle Organic Blobs */}
      <motion.div
        className="absolute top-0 left-0 w-[500px] h-[500px] rounded-full blur-3xl opacity-40"
        style={{ backgroundColor: '#ffc2d1' }}
        animate={{
          x: [0, 50, 0],
          y: [0, 30, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div
        className="absolute top-20 right-0 w-[450px] h-[450px] rounded-full blur-3xl opacity-35"
        style={{ backgroundColor: '#a7c7e7' }}
        animate={{
          x: [0, -40, 0],
          y: [0, 50, 0],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div
        className="absolute bottom-0 right-1/3 w-[550px] h-[550px] rounded-full blur-3xl opacity-30"
        style={{ backgroundColor: '#b4e7ce' }}
        animate={{
          x: [0, -30, 0],
          y: [0, -40, 0],
        }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Navigation */}
      <nav className="relative z-10 px-8 py-6 flex justify-between items-center backdrop-blur-sm">
        <div className="text-sm">
          <p className="font-light text-gray-800">agentic island</p>
          <p className="text-xs text-gray-500">designs</p>
        </div>
        <div className="flex gap-8 text-sm text-gray-700">
          <a href="#home" className="hover:text-gray-900 transition-colors">Home</a>
          <a href="#about" className="hover:text-gray-900 transition-colors">About</a>
          <a href="#contact" className="hover:text-gray-900 transition-colors">Contact</a>
        </div>
      </nav>

      {/* Main content */}
      <div id="home" className="relative z-10 max-w-5xl mx-auto px-8 pt-20 pb-32">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ scale: 1.05 }}
          className="inline-block mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-full text-sm bg-white/80 backdrop-blur-sm">
            <Sparkles className="w-4 h-4 text-gray-600" />
            <span className="text-gray-700">AI-Powered Romance Simulation</span>
          </div>
        </motion.div>

        {/* Main headline */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16"
        >
          <h1 className="text-6xl md:text-7xl lg:text-8xl leading-tight mb-8 font-serif text-gray-900">
            Experience your love story{" "}
            <motion.span
              className="inline-flex items-center"
              animate={{
                scale: [1, 1.1, 1],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <Heart className="w-16 h-16 md:w-20 md:h-20 text-rose-400 fill-rose-400 mx-2" />
            </motion.span>{" "}
            in a reality show{" "}
            <span className="italic">made just for you.</span>
          </h1>

          <p className="text-xl md:text-2xl max-w-3xl font-light leading-relaxed text-gray-600">
            Too Hot to Fine Tune.
          </p>
        </motion.div>

        {/* CTA Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <button
            onClick={() => router.push("/create")}
            className="group inline-flex items-center gap-3 px-8 py-4 bg-gray-900 text-white rounded-full hover:bg-gray-800 transition-all text-lg"
          >
            <span>Create Your Simulation</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </motion.div>

      </div>

      {/* About Section */}
      <div id="about" className="relative z-10 max-w-6xl mx-auto px-8 py-32">
        <div className="relative text-center mb-20">
          <h2 className="text-5xl md:text-6xl font-serif mb-4 text-gray-900">
            How It Works
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto font-light">
            Your personalized AI-powered dating simulation experience
          </p>
        </div>

        <div className="relative grid md:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="bg-white/60 backdrop-blur-sm p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-all"
            whileHover={{ y: -4 }}
          >
            <div className="w-16 h-16 bg-rose-100 rounded-2xl flex items-center justify-center mb-6">
              <Users className="w-8 h-8 text-rose-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900">
              Share Your Story
            </h3>
            <p className="text-gray-600 leading-relaxed text-sm">
              Tell us about yourself, your dating history, and what you're looking for in a partner. The more you share, the better your simulation!
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="bg-white/60 backdrop-blur-sm p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-all"
            whileHover={{ y: -4 }}
          >
            <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mb-6">
              <Zap className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900">
              AI Magic
            </h3>
            <p className="text-gray-600 leading-relaxed text-sm">
              Our AI analyzes your personality, preferences, and compatibility to create a custom reality show experience tailored just for you.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="bg-white/60 backdrop-blur-sm p-8 rounded-2xl border border-gray-200 hover:shadow-lg transition-all"
            whileHover={{ y: -4 }}
          >
            <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mb-6">
              <Star className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-3 text-gray-900">
              Watch Your Match
            </h3>
            <p className="text-gray-600 leading-relaxed text-sm">
              Experience a cinematic journey through personality analysis, compatibility matching, and your perfect date scenario!
            </p>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="relative mt-16 text-center"
        >
          <button
            onClick={() => router.push("/create")}
            className="inline-flex items-center gap-3 px-10 py-4 bg-gray-900 text-white rounded-full text-lg font-semibold hover:bg-gray-800 transition-all"
          >
            <Sparkles className="w-5 h-5" />
            Start Your Journey
            <ArrowRight className="w-5 h-5" />
          </button>
        </motion.div>
      </div>

      {/* Footer info */}
      <div id="contact" className="relative z-10 text-center py-16 border-t border-gray-200">
        <p className="text-xs text-gray-500 mb-2">Based in , Georgia, USA</p>
        <p className="text-xs text-gray-400">Agentic Island © 2026 • Too Hot to Fine Tune</p>
      </div>
    </div>
  );
}
