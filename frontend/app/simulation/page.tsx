"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'motion/react';
import { Heart, Sparkles, Flame, Star, ChevronLeft, ChevronRight } from 'lucide-react';

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

const scenes = [
  { title: 'CONTESTANT ENTRY' },
  { title: 'PERSONALITY ANALYSIS' },
  { title: 'COMPATIBILITY MATCHING' },
  { title: 'DATE SIMULATION' },
  { title: 'FINAL VERDICT' },
];

export default function SimulationPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<DatingProfile | null>(null);
  const [currentScene, setCurrentScene] = useState(0);

  useEffect(() => {
    const stored = sessionStorage.getItem('datingProfile');
    if (stored) {
      setProfile(JSON.parse(stored));
    } else {
      router.push('/create');
    }
  }, [router]);

  if (!profile) return null;

  const handleNext = () => {
    if (currentScene < scenes.length - 1) {
      setCurrentScene(currentScene + 1);
    } else {
      router.push('/feedback');
    }
  };

  const handlePrevious = () => {
    if (currentScene > 0) {
      setCurrentScene(currentScene - 1);
    }
  };

  const renderScene = () => {
    switch (currentScene) {
      case 0:
        return (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center space-y-6"
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
              className="w-32 h-32 mx-auto bg-rose-400 rounded-full flex items-center justify-center"
            >
              <Heart className="w-16 h-16 text-white" />
            </motion.div>
            <h2 className="text-5xl font-serif text-gray-900">{profile.name}</h2>
            <p className="text-2xl text-gray-600">{profile.age} years old • {profile.mbti}</p>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1 }}
              className="text-xl text-gray-700 italic max-w-md mx-auto font-light"
            >
              "{profile.relationshipGoal}"
            </motion.p>
          </motion.div>
        );

      case 1:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center space-y-8"
          >
            <h2 className="text-4xl font-serif text-gray-900">Analyzing Personality...</h2>
            <div className="grid grid-cols-2 gap-4 max-w-xl mx-auto">
              {[
                { label: 'Love Language', value: profile.loveLanguage },
                { label: 'MBTI', value: profile.mbti },
                { label: 'Relationship Style', value: 'Analyzing...' },
                { label: 'Compatibility Score', value: '94%' },
              ].map((item, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.3 }}
                  className="bg-white/70 backdrop-blur-sm p-6 rounded-xl border border-gray-200"
                >
                  <p className="text-sm text-gray-500 mb-1">{item.label}</p>
                  <p className="text-lg font-medium text-gray-900">{item.value}</p>
                </motion.div>
              ))}
            </div>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="flex justify-center gap-2"
            >
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-6 h-6 text-yellow-500 fill-yellow-500" />
              ))}
            </motion.div>
          </motion.div>
        );

      case 2:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center space-y-8"
          >
            <h2 className="text-4xl font-serif text-gray-900">Finding Your Perfect Match...</h2>
            <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
              {['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley'].map((name, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.2 }}
                  className={`relative p-6 rounded-xl ${
                    i === 2
                      ? 'bg-gray-900 text-white ring-2 ring-gray-700'
                      : 'bg-white/70 backdrop-blur-sm border border-gray-200'
                  }`}
                >
                  <div className={`w-16 h-16 mx-auto ${i === 2 ? 'bg-white/20' : 'bg-gray-200'} rounded-full mb-3`} />
                  <p className={`font-medium ${i === 2 ? 'text-white' : 'text-gray-900'}`}>{name}</p>
                  <p className={`text-sm ${i === 2 ? 'text-white/80' : 'text-gray-600'}`}>
                    {i === 2 ? '98% Match!' : `${70 + i * 4}%`}
                  </p>
                  {i === 2 && (
                    <div className="absolute -top-2 -right-2">
                      <Sparkles className="w-6 h-6 text-white" />
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        );

      case 3:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center space-y-6"
          >
            <h2 className="text-4xl font-serif text-gray-900">Your Dream Date</h2>

            {/* Video Section */}
            <motion.div
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              className="bg-white/70 backdrop-blur-sm p-6 rounded-2xl border border-gray-200 max-w-3xl mx-auto"
            >
              <div className="aspect-video bg-gradient-to-br from-pink-50 to-purple-50 rounded-lg flex items-center justify-center border border-purple-100">
                <div className="text-center space-y-4">
                  <div className="w-20 h-20 mx-auto bg-white rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300 cursor-pointer">
                    <div className="w-0 h-0 border-t-8 border-t-transparent border-l-12 border-l-rose-400 border-b-8 border-b-transparent ml-1" />
                  </div>
                  <p className="text-gray-700 font-medium">Watch Your Date Unfold</p>
                  <p className="text-sm text-gray-500 max-w-md mx-auto italic">
                    "{profile.idealDate}"
                  </p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        );

      case 4:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center space-y-6 max-w-4xl mx-auto"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', duration: 1 }}
            >
              <h2 className="text-4xl font-serif text-gray-900 mb-2">
                Your Love Life Analysis
              </h2>
              <p className="text-lg text-gray-600">Here's what we discovered, {profile.name}</p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Pros / Strengths */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white/70 backdrop-blur-sm p-6 rounded-xl border border-green-200 text-left"
              >
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                    <Star className="w-5 h-5 text-green-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900">Your Strengths</h3>
                </div>
                <ul className="space-y-3">
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">✓</span>
                    <span className="text-gray-700">Strong {profile.loveLanguage} love language</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">✓</span>
                    <span className="text-gray-700">Clear relationship goals</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">✓</span>
                    <span className="text-gray-700">Knows what you want in a partner</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-green-600 mt-1">✓</span>
                    <span className="text-gray-700">98% compatibility potential</span>
                  </li>
                </ul>
              </motion.div>

              {/* Cons / Areas to Improve */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
                className="bg-white/70 backdrop-blur-sm p-6 rounded-xl border border-pink-200 text-left"
              >
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-8 h-8 bg-pink-100 rounded-full flex items-center justify-center">
                    <Heart className="w-5 h-5 text-pink-600" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900">Growth Areas</h3>
                </div>
                <ul className="space-y-3">
                  <li className="flex items-start gap-2">
                    <span className="text-pink-600 mt-1">→</span>
                    <span className="text-gray-700">Be mindful of: {profile.dealbreakers}</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-pink-600 mt-1">→</span>
                    <span className="text-gray-700">Learn from past experiences</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-pink-600 mt-1">→</span>
                    <span className="text-gray-700">Stay open to new connections</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-pink-600 mt-1">→</span>
                    <span className="text-gray-700">Communicate your needs clearly</span>
                  </li>
                </ul>
              </motion.div>
            </div>

            {/* Overall Verdict */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7 }}
              className="bg-gray-900 text-white p-6 rounded-xl"
            >
              <Star className="w-12 h-12 mx-auto mb-3 fill-white" />
              <p className="text-xl font-medium mb-2">You're Ready for Love!</p>
              <p className="text-white/80">Your simulation shows great compatibility potential with your ideal match.</p>
            </motion.div>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-full min-h-screen p-8 flex flex-col items-center justify-center relative overflow-hidden" style={{ backgroundColor: '#f5f1ed' }}>
      {/* Subtle Organic Blobs */}
      <div
        className="absolute top-0 left-0 w-[500px] h-[500px] rounded-full blur-3xl opacity-35"
        style={{ backgroundColor: '#ffc2d1' }}
      />
      <div
        className="absolute top-20 right-0 w-[450px] h-[450px] rounded-full blur-3xl opacity-30"
        style={{ backgroundColor: '#a7c7e7' }}
      />
      <div
        className="absolute bottom-0 right-1/3 w-[550px] h-[550px] rounded-full blur-3xl opacity-25"
        style={{ backgroundColor: '#b4e7ce' }}
      />

      {/* Scene title banner */}
      <motion.div
        key={currentScene}
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="absolute top-8 left-1/2 -translate-x-1/2 bg-gray-900 backdrop-blur-sm px-8 py-3 rounded-full"
      >
        <p className="text-white font-medium tracking-wider text-sm">{scenes[currentScene]?.title}</p>
      </motion.div>

      {/* Main content */}
      <div className="relative z-10 w-full max-w-4xl">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentScene}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
          >
            {renderScene()}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation arrows */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4">
        <button
          onClick={handlePrevious}
          disabled={currentScene === 0}
          className="p-3 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white hover:scale-110 transition-all disabled:opacity-30 disabled:hover:scale-100 disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-6 h-6 text-gray-900" />
        </button>

        {/* Progress indicator */}
        <div className="flex gap-2">
          {scenes.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentScene
                  ? 'bg-gray-900 w-8'
                  : index < currentScene
                  ? 'bg-gray-500'
                  : 'bg-gray-300'
              }`}
            />
          ))}
        </div>

        <button
          onClick={handleNext}
          className="p-3 bg-gray-900 rounded-full hover:bg-gray-800 hover:scale-110 transition-all"
        >
          <ChevronRight className="w-6 h-6 text-white" />
        </button>
      </div>
    </div>
  );
}
