import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Upload, Home, Video, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import professorMascot from "@/assets/professor-mascot.png";

const Lecturer = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  // Dialog states
  const [notesDialogOpen, setNotesDialogOpen] = useState(false);
  const [characterDialogOpen, setCharacterDialogOpen] = useState(false);
  const [videoDialogOpen, setVideoDialogOpen] = useState(false);
  
  // Form data
  const [question, setQuestion] = useState("");
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [fileToUpload, setFileToUpload] = useState(null);
  const [characterName, setCharacterName] = useState("");
  const [characterPersonality, setCharacterPersonality] = useState("");
  const [characterVoice, setCharacterVoice] = useState("");
  
  // Generation state
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideoUrl, setGeneratedVideoUrl] = useState("");

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadedFileName(file.name);
    setFileToUpload(file);
  };

  const handleNotesSubmit = () => {
    if (!uploadedFileName.trim()) {
      toast({
        title: "No content",
        description: "Please upload or paste lecture notes.",
        variant: "destructive",
      });
      return;
    }
    
    setNotesDialogOpen(false);
    setCharacterDialogOpen(true);
  };

  const handleGenerateVideo = async () => {
    if (!characterName.trim()) {
      toast({
        title: "Missing character name",
        description: "Please provide a character name.",
        variant: "destructive",
      });
      return;
    }

    setCharacterDialogOpen(false);
    setIsGenerating(true);
    
    // Backend call to generate video
     try {
    // Build form data for both file + other params
    const formData = new FormData();
    formData.append("file", fileToUpload);
    formData.append("question",question);
    formData.append("character_name", characterName);
    formData.append("character_personality", characterPersonality);
    formData.append("voice_style", characterVoice);

    const response = await fetch("http://localhost:5000/generate", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("🎥 Video generation started:", data);

    toast({
      title: "Generating video...",
      description: "Your lecture video is being created. This may take a moment.",
    });
  } catch (error) {
    console.error("Error generating video:", error);
    toast({
      title: "Error generating video",
      description: error.message,
      variant: "destructive",
    });
  } finally {
    setIsGenerating(false);
  }
    
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 bg-card/30 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src={professorMascot} alt="Professor" className="w-12 h-12" />
            <h1 className="text-2xl font-bold">
              <span className="text-primary">AI</span> Lecturer
            </h1>
          </div>
          <Button variant="ghost" onClick={() => navigate("/")} className="gap-2">
            <Home className="w-4 h-4" />
            Home
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <img src={professorMascot} alt="Professor" className="w-48 h-48 mx-auto" />
          
          <div className="space-y-4">
            <h2 className="text-4xl font-bold">
              Create Your <span className="text-primary">AI Lecture Video</span>
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Upload your lecture notes, customize your AI lecturer character, and generate an engaging video presentation.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button 
              variant="hero" 
              size="lg" 
              className="gap-2 px-8"
              onClick={() => setNotesDialogOpen(true)}
            >
              <Upload className="w-5 h-5" />
              Upload Lecture Notes
            </Button>
          </div>

          {isGenerating && (
            <div className="bg-card/50 border border-border/50 rounded-2xl p-8 space-y-4">
              <div className="flex items-center justify-center gap-3">
                <Sparkles className="w-6 h-6 text-primary animate-pulse" />
                <p className="text-lg font-medium">Generating your AI lecture video...</p>
              </div>
              <div className="flex gap-2 justify-center">
                <div className="w-3 h-3 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-3 h-3 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-3 h-3 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Lecture Notes Dialog */}
      <Dialog open={notesDialogOpen} onOpenChange={setNotesDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5 text-primary" />
              Upload Lecture Notes
            </DialogTitle>
            <DialogDescription>
              Upload a file or paste your lecture notes directly to get started.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="relative">
              <input
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload-dialog"
              />
              <label htmlFor="file-upload-dialog">
                <Button
                  variant="outline"
                  className="w-full border-primary/50 hover:border-primary cursor-pointer"
                  asChild
                >
                  <div>
                    <Upload className="mr-2 w-4 h-4" />
                    Choose File
                  </div>
                </Button>
              </label>
            </div>

            {uploadedFileName && (
              <div className="p-3 bg-primary/10 rounded-lg border border-primary/30">
                <p className="text-sm font-medium text-primary truncate">
                  📄 {uploadedFileName}
                </p>
              </div>
            )}

            <div className="relative">
              <p className="text-sm text-muted-foreground mb-2">Ask Question about lecture notes for AI to answer:</p>
              <Textarea
                placeholder="Enter your question here..."
                className="min-h-[250px] bg-background/50"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </div>

            
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setNotesDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="hero" onClick={handleNotesSubmit}>
              Next: Character Details
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Character Details Dialog */}
      <Dialog open={characterDialogOpen} onOpenChange={setCharacterDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              Customize Your AI Lecturer
            </DialogTitle>
            <DialogDescription>
              Define the character that will present your lecture notes.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Character</label>
              <Input
                placeholder="e.g., Hello Kitty, Chiikawa..."
                value={characterName}
                onChange={(e) => setCharacterName(e.target.value)}
                className="bg-background/50"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Personality Traits</label>
              <Textarea
                placeholder="e.g., Enthusiastic, clear, patient, encouraging..."
                value={characterPersonality}
                onChange={(e) => setCharacterPersonality(e.target.value)}
                className="min-h-[100px] bg-background/50"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Voice Style (Optional)</label>
              <Input
                placeholder="e.g., Warm and friendly, Professional, Energetic..."
                value={characterVoice}
                onChange={(e) => setCharacterVoice(e.target.value)}
                className="bg-background/50"
              />
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => {
              setCharacterDialogOpen(false);
              setNotesDialogOpen(true);
            }}>
              Back
            </Button>
            <Button variant="hero" onClick={handleGenerateVideo} className="gap-2">
              <Video className="w-4 h-4" />
              Generate Video
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Video Result Dialog */}
      <Dialog open={videoDialogOpen} onOpenChange={setVideoDialogOpen}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Video className="w-5 h-5 text-primary" />
              Your AI Lecture Video
            </DialogTitle>
            <DialogDescription>
              Watch your generated lecture video below.
            </DialogDescription>
          </DialogHeader>
          
          <div className="py-4">
            <div className="aspect-video bg-black rounded-lg overflow-hidden">
              <video
                controls
                className="w-full h-full"
                src={generatedVideoUrl}
              >
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => {
              setVideoDialogOpen(false);
              setQuestion("");
              setUploadedFileName("");
              setCharacterName("");
              setCharacterPersonality("");
              setCharacterVoice("");
              setGeneratedVideoUrl("");
            }}>
              Create Another
            </Button>
            <Button variant="hero" onClick={() => {
              const a = document.createElement('a');
              a.href = generatedVideoUrl;
              a.download = 'ai-lecture.mp4';
              a.click();
            }}>
              Download Video
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Lecturer;
