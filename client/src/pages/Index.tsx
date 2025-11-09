import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { BookOpen, Upload, Sparkles, ArrowRight } from "lucide-react";
import heroBackground from "@/assets/hero-background.png";
import professorMascot from "@/assets/professor-mascot.png";
import duckImage from "@/assets/duck.png";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section
        className="relative min-h-screen flex items-center justify-center overflow-hidden"
        style={{
          // backgroundImage: `linear-gradient(to bottom, rgba(33, 42, 52, 0.95), rgba(33, 42, 52, 0.85)), url(${heroBackground})`,
          background: "radial-gradient(circle at top, #1e3a8a, #0f172a)",
          // backgroundImage: `linear-gradient(to bottom right, rgba(204, 255, 204, 0.95), rgba(224, 255, 229, 0.9), rgba(230, 250, 255, 0.8))`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Falling shooting stars */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none z-10">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="shooting-star"
              style={{
                left: `${10 + Math.random() * 80}%`, // horizontal spread
                top: `${-50 + Math.random() * 50}px`, // slightly above the hero section
                animationDuration: `${1.5 + Math.random() * 1.5}s`,
                animationDelay: `${i * 1.5}s`,
              }}
            />
          ))}
        </div>

        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/20 to-background pointer-events-none" />

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            {/* SBUHACKS Badge */}
            <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-card/50 backdrop-blur-sm border border-primary/30 mb-8 animate-pulse">
              <Sparkles className="w-5 h-5 text-primary" />
              <span className="text-sm font-bold text-primary tracking-wider">SBUHACKS 2025</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-6xl md:text-8xl font-black mb-6 tracking-tight">
              <span className="bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
                Professor QuAIck
              </span>
            </h1>

            <p className="text-xl md:text-2xl text-foreground/90 mb-4 max-w-3xl mx-auto leading-relaxed">
              Transform Your Lecture Notes Into Interactive Lesson
            </p>

            <p className="text-md md:text-lg text-muted-foreground mb-12 max-w-2xl mx-auto">
              Learn with Prof. QuAIck by uploading your notes and turning them into interactive video lessons that help you understand faster, study smarter, and ace your next midterm!
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <Button
                variant="hero"
                size="lg"
                className="text-lg px-8 py-6 h-auto"
                onClick={() => navigate("/lecturer")}
              >
                Start Learning Now
                <ArrowRight className="ml-2" />
              </Button>

              <Button
                variant="outline"
                size="lg"
                className="text-lg px-8 py-6 h-auto border-primary/50 hover:border-primary"
              >
                <BookOpen className="mr-2" />
                Learn More
              </Button>
            </div>

            {/* Mascot */}
            <div className="flex justify-center">
              <img
                src={professorMascot}
                alt="AI Professor Mascot"
                className="w-48 h-48 md:w-64 md:h-64 drop-shadow-2xl animate-bounce"
                style={{ animationDuration: '3s' }}
              />
            </div>
            <div className="absolute bottom-10 w-full overflow-hidden">
              <div className="flex animate-duckTrain space-x-8">
                {Array.from({ length: 15 }).map((_, i) => (
                  <img
                    key={i}
                    src={duckImage}
                    alt="Duck"
                    className="w-16 h-16 md:w-20 md:h-20"
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>


      {/* Features Section */}
      <section className="py-24 bg-card/30">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-16">
            How It <span className="text-primary">Works</span>
          </h2>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-card p-8 rounded-2xl border border-border hover:border-primary/50 transition-all hover:shadow-glow">
              <div className="w-16 h-16 bg-primary/20 rounded-xl flex items-center justify-center mb-6">
                <Upload className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Upload Notes</h3>
              <p className="text-muted-foreground">
                Simply upload your lecture notes, PDFs, or documents to get started
              </p>
            </div>

            <div className="bg-card p-8 rounded-2xl border border-border hover:border-secondary/50 transition-all hover:shadow-glow">
              <div className="w-16 h-16 bg-secondary/20 rounded-xl flex items-center justify-center mb-6">
                <Sparkles className="w-8 h-8 text-secondary" />
              </div>
              <h3 className="text-2xl font-bold mb-4">AI Processing</h3>
              <p className="text-muted-foreground">
                Our AI analyzes and understands your content in seconds
              </p>
            </div>

            <div className="bg-card p-8 rounded-2xl border border-border hover:border-accent/50 transition-all hover:shadow-glow">
              <div className="w-16 h-16 bg-accent/20 rounded-xl flex items-center justify-center mb-6">
                <BookOpen className="w-8 h-8 text-accent" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Learn Interactively</h3>
              <p className="text-muted-foreground">
                Ask questions and get personalized explanations from your AI professor
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-border/50">
        <div className="container mx-auto px-4 text-center">
          <p className="text-muted-foreground">
            Built for <span className="text-primary font-bold">SBUHACKS 2025</span> @ Stony Brook University
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            November 7-9, 2025
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
