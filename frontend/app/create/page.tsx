"use client";

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Heart, ArrowLeft, Sparkles, User, Brain, Target, X, Clock, MessageCircle } from 'lucide-react';
import { motion, useScroll, useTransform } from 'motion/react';

interface DatingProfile {
  name: string;
  age: string;
  mbti: string;
  relationshipGoal: string;
  dealbreakers: string;
  pastRelationships: string;
  loveLanguage: string;
  idealDate: string;
}

export default function CreatePage() {
  const router = useRouter();
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  const gradientY = useTransform(scrollYProgress, [0, 1], ['0%', '100%']);

  const [profile, setProfile] = useState<DatingProfile>({
    name: '',
    age: '',
    mbti: '',
    relationshipGoal: '',
    dealbreakers: '',
    pastRelationships: '',
    loveLanguage: '',
    idealDate: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Store profile in sessionStorage for the simulation page
    sessionStorage.setItem('datingProfile', JSON.stringify(profile));
    router.push('/simulation');
  };

  const updateField = (field: keyof DatingProfile, value: string) => {
    setProfile({ ...profile, [field]: value });
  };

  return (
    <div ref={containerRef} className="min-h-screen relative overflow-hidden" style={{ position: 'relative', backgroundColor: '#f5f1ed' }}>
      {/* Subtle Organic Blobs */}
      <div
        className="absolute top-0 right-0 w-[500px] h-[500px] rounded-full blur-3xl opacity-35"
        style={{ backgroundColor: '#ffc2d1' }}
      />
      <div
        className="absolute bottom-0 left-0 w-[450px] h-[450px] rounded-full blur-3xl opacity-30"
        style={{ backgroundColor: '#c4b5fd' }}
      />
      <div
        className="absolute top-1/3 left-1/4 w-[400px] h-[400px] rounded-full blur-3xl opacity-25"
        style={{ backgroundColor: '#a7c7e7' }}
      />

      {/* Navigation */}
      <motion.nav
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 px-8 py-6"
      >
        <button
          onClick={() => router.push('/')}
          className="flex items-center gap-2 text-sm hover:text-rose-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </button>
      </motion.nav>

      {/* Form content */}
      <div className="relative z-10 max-w-3xl mx-auto px-8 py-12">
        <motion.div
          className="mb-12 text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="inline-flex items-center gap-2 mb-4">
            <Heart className="w-8 h-8 text-rose-400" />
            <h1 className="text-5xl font-serif text-gray-900">Agentic Island</h1>
            <Sparkles className="w-8 h-8 text-gray-600" />
          </div>
          <p className="text-xl text-gray-600 font-light">Too Hot to Fine Tune</p>
          <p className="text-sm text-gray-500 mt-4">Fill out your profile to generate your personalized simulation</p>
        </motion.div>

        <motion.form
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="space-y-6 bg-white/70 backdrop-blur-sm p-10 rounded-2xl border border-gray-200 shadow-lg relative"
        >
          <motion.div
            className="grid grid-cols-2 gap-6"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <div className="relative">
              <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                <User className="w-4 h-4 text-rose-500" />
                Name
              </label>
              <motion.input
                type="text"
                value={profile.name}
                onChange={(e) => updateField('name', e.target.value)}
                className="w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-400 focus:border-transparent transition-all"
                placeholder="Your name"
                required
              />
            </div>
            <div className="relative">
              <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                <Clock className="w-4 h-4 text-purple-500" />
                Age
              </label>
              <motion.input
                type="number"
                value={profile.age}
                onChange={(e) => updateField('age', e.target.value)}
                className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all shadow-sm"
                placeholder="25"
                required
              />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <Brain className="w-4 h-4 text-blue-500" />
              MBTI Type
            </label>
            <motion.input
              type="text"
              value={profile.mbti}
              onChange={(e) => updateField('mbti', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-blue-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition-all shadow-sm"
              placeholder="ENFP, INTJ, etc."
              maxLength={4}
              required
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <Heart className="w-4 h-4 text-pink-500" />
              Love Language
            </label>
            <motion.select
              value={profile.loveLanguage}
              onChange={(e) => updateField('loveLanguage', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-pink-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400 transition-all shadow-sm"
              required
            >
              <option value="">Select...</option>
              <option value="Words of Affirmation">Words of Affirmation</option>
              <option value="Quality Time">Quality Time</option>
              <option value="Receiving Gifts">Receiving Gifts</option>
              <option value="Acts of Service">Acts of Service</option>
              <option value="Physical Touch">Physical Touch</option>
            </motion.select>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <Target className="w-4 h-4 text-green-500" />
              Relationship Goal
            </label>
            <motion.textarea
              value={profile.relationshipGoal}
              onChange={(e) => updateField('relationshipGoal', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-green-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-green-400 resize-none transition-all shadow-sm"
              placeholder="What are you looking for in a relationship?"
              rows={3}
              required
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.25 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <MessageCircle className="w-4 h-4 text-indigo-500" />
              Past Dating History
            </label>
            <motion.textarea
              value={profile.pastRelationships}
              onChange={(e) => updateField('pastRelationships', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-indigo-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 resize-none transition-all shadow-sm"
              placeholder="Tell us about your relationship history..."
              rows={3}
              required
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <X className="w-4 h-4 text-red-500" />
              Deal Breakers
            </label>
            <motion.textarea
              value={profile.dealbreakers}
              onChange={(e) => updateField('dealbreakers', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-red-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-red-400 resize-none transition-all shadow-sm"
              placeholder="What are your absolute no-gos?"
              rows={2}
              required
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.35 }}
          >
            <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
              <Sparkles className="w-4 h-4 text-amber-500" />
              Ideal Date Scenario
            </label>
            <motion.textarea
              value={profile.idealDate}
              onChange={(e) => updateField('idealDate', e.target.value)}
              className="w-full px-4 py-3 bg-white/90 backdrop-blur-sm border-2 border-amber-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-400 resize-none transition-all shadow-sm"
              placeholder="Describe your dream date..."
              rows={3}
              required
            />
          </motion.div>

          <motion.button
            type="submit"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.4 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-4 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 text-lg"
          >
            <Heart className="w-5 h-5" />
            Generate My Simulation
          </motion.button>
        </motion.form>
      </div>
    </div>
  );
}
