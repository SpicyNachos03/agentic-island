"use client";

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Heart, ArrowLeft, Sparkles, User, Brain, Target, X, Clock, MessageCircle } from 'lucide-react';
import { motion, useScroll, useTransform } from 'motion/react';
import { Card } from '../../components/ui/card';

interface DatingProfile {
  name: string;
  age: string;
  mbti: string;
  relationshipGoal: string;
  dealbreakers: string;
  pastRelationships: string;
  loveLanguage: string;
  idealDate: string;
  greenFlags: string;
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
    greenFlags: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sessionStorage.setItem('datingProfile', JSON.stringify(profile));
    router.push('/simulation');
  };

  const updateField = (field: keyof DatingProfile, value: string) => {
    setProfile({ ...profile, [field]: value });
  };

  return (
    <div ref={containerRef} className="min-h-screen relative overflow-hidden" style={{ position: 'relative', backgroundColor: '#f5f1ed' }}>
      {/* Subtle Organic Blobs */}
      <motion.div
        className="absolute top-0 right-0 w-[500px] h-[500px] rounded-full blur-3xl opacity-35"
        style={{ backgroundColor: '#ffc2d1', y: useTransform(scrollYProgress, [0, 1], [0, 150]) }}
        animate={{
          scale: [1, 1.3, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div
        className="absolute bottom-0 left-0 w-[450px] h-[450px] rounded-full blur-3xl opacity-30"
        style={{ backgroundColor: '#c4b5fd', y: useTransform(scrollYProgress, [0, 1], [0, -100]) }}
        animate={{
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />
      <motion.div
        className="absolute top-1/3 left-1/4 w-[400px] h-[400px] rounded-full blur-3xl opacity-25"
        style={{ backgroundColor: '#a7c7e7' }}
        animate={{
          x: [0, 60, 0],
          y: [0, -40, 0],
        }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Navigation */}
      <nav className="relative z-10 px-8 py-6">
        <button
          onClick={() => router.push('/')}
          className="flex items-center gap-2 text-sm hover:text-rose-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </button>
      </nav>

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

        <form onSubmit={handleSubmit} className="relative">
          {/* Bento Box Grid - 12 column system for precise control */}
          <div className="relative grid grid-cols-1 md:grid-cols-12 gap-4 auto-rows-auto">

            {/* Row 1: Name (50%), Age (25%), MBTI (25%) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4 }}
              className="md:col-span-6"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-rose-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <User className="w-4 h-4 text-rose-500" />
                  Name
                </label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => updateField('name', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-rose-400 focus:border-transparent transition-all"
                  placeholder="Your name"
                  required
                />
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.05 }}
              className="md:col-span-3"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-purple-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Clock className="w-4 h-4 text-purple-500" />
                  Age
                </label>
                <input
                  type="number"
                  value={profile.age}
                  onChange={(e) => updateField('age', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-transparent transition-all"
                  placeholder="25"
                  required
                />
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.1 }}
              className="md:col-span-3"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-blue-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Brain className="w-4 h-4 text-blue-500" />
                  MBTI
                </label>
                <input
                  type="text"
                  value={profile.mbti}
                  onChange={(e) => updateField('mbti', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition-all"
                  placeholder="ENFP"
                  maxLength={4}
                  required
                />
              </Card>
            </motion.div>

            {/* Row 2: Love Language (100%) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.15 }}
              className="md:col-span-12"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-pink-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Heart className="w-4 h-4 text-pink-500" />
                  Love Language
                </label>
                <select
                  value={profile.loveLanguage}
                  onChange={(e) => updateField('loveLanguage', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all"
                  required
                >
                  <option value="">Select...</option>
                  <option value="Words of Affirmation">Words of Affirmation</option>
                  <option value="Quality Time">Quality Time</option>
                  <option value="Receiving Gifts">Receiving Gifts</option>
                  <option value="Acts of Service">Acts of Service</option>
                  <option value="Physical Touch">Physical Touch</option>
                </select>
              </Card>
            </motion.div>

            {/* Row 3: Relationship Goal (40%), Deal Breakers (60%) */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.2 }}
              className="md:col-span-5"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-green-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Target className="w-4 h-4 text-green-500" />
                  Relationship Goal
                </label>
                <textarea
                  value={profile.relationshipGoal}
                  onChange={(e) => updateField('relationshipGoal', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent resize-none transition-all"
                  placeholder="What are you looking for in a relationship?"
                  rows={5}
                  required
                />
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.25 }}
              className="md:col-span-7"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-red-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <X className="w-4 h-4 text-red-500" />
                  Deal Breakers
                </label>
                <textarea
                  value={profile.dealbreakers}
                  onChange={(e) => updateField('dealbreakers', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent resize-none transition-all"
                  placeholder="What are your absolute no-gos?"
                  rows={5}
                  required
                />
              </Card>
            </motion.div>

            {/* Row 4: Past Dating History (55%) - tall, spans 2 rows */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.3 }}
              className="md:col-span-7 md:row-span-2"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-indigo-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <MessageCircle className="w-4 h-4 text-indigo-500" />
                  Past Dating History
                </label>
                <textarea
                  value={profile.pastRelationships}
                  onChange={(e) => updateField('pastRelationships', e.target.value)}
                  className="w-full h-[calc(100%-3rem)] px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent resize-none transition-all"
                  placeholder="Tell us about your relationship history..."
                  required
                />
              </Card>
            </motion.div>

            {/* Ideal Date Scenario (45%) - top right */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.35 }}
              className="md:col-span-5"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-amber-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Sparkles className="w-4 h-4 text-amber-500" />
                  Ideal Date Scenario
                </label>
                <textarea
                  value={profile.idealDate}
                  onChange={(e) => updateField('idealDate', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-transparent resize-none transition-all"
                  placeholder="Describe your dream date..."
                  rows={3}
                  required
                />
              </Card>
            </motion.div>

            {/* Green Flags (45%) - bottom right */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: 0.4 }}
              className="md:col-span-5"
            >
              <Card className="p-6 bg-white/70 backdrop-blur-sm border-emerald-200 hover:shadow-lg transition-all h-full">
                <label className="flex items-center gap-2 text-sm font-medium mb-2 text-gray-700">
                  <Heart className="w-4 h-4 text-emerald-500" />
                  Green Flags
                </label>
                <textarea
                  value={profile.greenFlags}
                  onChange={(e) => updateField('greenFlags', e.target.value)}
                  className="w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:border-transparent resize-none transition-all"
                  placeholder="What qualities do you look for in a partner?"
                  rows={3}
                  required
                />
              </Card>
            </motion.div>

          </div>

          {/* Submit Button */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="mt-6"
          >
            <button
              type="submit"
              className="w-full py-4 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 hover:scale-[1.02] transition-all flex items-center justify-center gap-2 text-lg shadow-lg"
            >
              <Heart className="w-5 h-5" />
              Generate My Simulation
            </button>
          </motion.div>
        </form>
      </div>
    </div>
  );
}
