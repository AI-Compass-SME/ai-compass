import React, { useEffect, useState, useMemo } from 'react';
import { PageBackground } from '@/components/ui/PageBackground';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, SkipForward, ArrowRight, CheckCircle2, Circle, Disc, Check, Menu, Compass } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export default function QuestionnaireWizard() {
    const { responseId } = useParams();
    const navigate = useNavigate();
    const [questions, setQuestions] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [selectedAnswers, setSelectedAnswers] = useState([]);
    // Map<questionId, Array<answerId>>
    const [allAnswers, setAllAnswers] = useState({});

    // Track answered questions for progress calculation
    // Map<questionId, boolean>
    const [answeredMap, setAnsweredMap] = useState({});

    // Load progress from local storage on mount
    useEffect(() => {
        const savedProgress = localStorage.getItem(`assessment_progress_${responseId}`);
        if (savedProgress) {
            try {
                const { index, answered, answers } = JSON.parse(savedProgress);
                if (typeof index === 'number') setCurrentIndex(index);
                if (answered) setAnsweredMap(answered);
                if (answers) setAllAnswers(answers);
            } catch (e) {
                console.error("Failed to parse saved progress", e);
            }
        }
    }, [responseId]);

    // Set page title
    useEffect(() => {
        document.title = "AI Compass: Assessment";
    }, []);

    // Save progress to local storage
    useEffect(() => {
        if (questions.length > 0) {
            localStorage.setItem(`assessment_progress_${responseId}`, JSON.stringify({
                index: currentIndex,
                answered: answeredMap,
                answers: allAnswers
            }));
        }
    }, [currentIndex, answeredMap, allAnswers, questions.length, responseId]);

    useEffect(() => {
        async function fetchQuestions() {
            try {
                // 1. Try Cache
                // 1. Try Cache
                const cached = sessionStorage.getItem('cached_questionnaire_data_v3');
                if (cached) {
                    console.log("Found cached data in sessionStorage");
                    try {
                        const data = JSON.parse(cached);
                        console.log("Parsed cached data:", data);
                        if (data && data.questions && Array.isArray(data.questions)) {
                            console.log(`Using cached questionnaire with ${data.questions.length} questions.`);
                            setQuestions(data.questions);
                            setLoading(false);
                            return;
                        } else {
                            console.warn("Cached data format invalid:", data);
                        }
                    } catch (e) {
                        console.error("Failed to parse cached questionnaire:", e);
                    }
                } else {
                    console.log("No cached questionnaire found in sessionStorage.");
                }

                // 2. Fallback to Network
                const data = await api.getQuestionnaire();
                if (data && data.questions) {
                    setQuestions(data.questions);
                    // Update cache for persistence on refresh
                    sessionStorage.setItem('cached_questionnaire_data_v3', JSON.stringify(data));
                }
            } catch (error) {
                console.error("Failed to load questions", error);
                toast.error("Failed to load questionnaire.");
            } finally {
                setLoading(false);
            }
        }
        fetchQuestions();
    }, []);

    useEffect(() => {
        const currentQ = questions[currentIndex];
        if (!currentQ) return;

        // 1. Check if we have a persisted answer in our local session state
        if (allAnswers[currentQ.question_id] && allAnswers[currentQ.question_id].length > 0) {
            setSelectedAnswers(allAnswers[currentQ.question_id]);
            return;
        }

        // 2. Fallback: Pre-select slider default if applicable and no previous answer
        if ((currentQ.type || 'choice').toLowerCase() === 'slider' && currentQ.answers?.length > 0) {
            // Default to the first option (or middle/semantic default if we had one)
            setSelectedAnswers([currentQ.answers[0].answer_id]);
        } else {
            setSelectedAnswers([]);
        }
    }, [currentIndex, questions, allAnswers]);

    // Group questions by dimension
    const dimensions = useMemo(() => {
        if (!questions.length) return [];

        const groups = {};
        questions.forEach(q => {
            const dId = q.dimension_id || 0;
            if (!groups[dId]) {
                groups[dId] = {
                    id: dId,
                    name: q.dimension_name || `Dimension ${dId}`,
                    questions: [],
                    total: 0,
                    answered: 0
                };
            }
            groups[dId].questions.push(q);
            groups[dId].total++;
            if (answeredMap[q.question_id]) {
                groups[dId].answered++;
            }
        });

        // Convert to array and sort by ID
        return Object.values(groups).sort((a, b) => a.id - b.id);
    }, [questions, answeredMap]);

    const handleNext = async () => {
        // Validation skip for slider is implicit if we pre-select, but good safety check
        if (selectedAnswers.length === 0) {
            const currentQ = questions[currentIndex];
            if ((currentQ.type || 'choice').toLowerCase() === 'slider') {
                // Should be pre-selected, but just in case
            } else {
                toast.warning("Please select an answer to continue.");
                return;
            }
        }

        if (saving) return;
        setSaving(true);

        try {
            const currentQ = questions[currentIndex];
            // Only save to DB if we have answers (for slider/choice)
            if (selectedAnswers.length > 0) {
                await api.saveAnswer(parseInt(responseId), currentQ.question_id, selectedAnswers);
            }

            // Mark as answered locally for progress bar and persistence
            setAnsweredMap(prev => ({ ...prev, [currentQ.question_id]: true }));
            setAllAnswers(prev => ({ ...prev, [currentQ.question_id]: selectedAnswers }));

            if (currentIndex < questions.length - 1) {
                setCurrentIndex(prev => prev + 1);
            } else {
                // Do NOT complete assessment yet. Navigate to Company Snapshot for details.
                toast.success("Questions complete! Just one last step.");
                navigate('/snapshot');
            }
        } catch (error) {
            console.error("Failed to save answer", error);
            if (error.message && (error.message.includes("404") || error.message.toLowerCase().includes("not found"))) {
                toast.error("Session expired. Please start over.");
                navigate('/');
                return;
            }
            toast.error(error.message || "Failed to save answer.");
        } finally {
            setSaving(false);
        }
    };

    const toggleCheckbox = (answerId) => {
        setSelectedAnswers(prev =>
            prev.includes(answerId)
                ? prev.filter(id => id !== answerId)
                : [...prev, answerId]
        );
    };

    const handleRadioChange = (val) => {
        const ansId = parseInt(val);
        setSelectedAnswers([ansId]);
    };

    const handleSliderChange = (val) => {
        const index = val[0];
        if (questions[currentIndex].answers[index]) {
            setSelectedAnswers([questions[currentIndex].answers[index].answer_id]);
        }
    };

    const handleSkipDimension = async () => {
        if (saving) return;
        setSaving(true);
        try {
            const remaining = questions.slice(currentIndex);
            const d8Questions = remaining.filter(q => q.dimension_id === 8);

            await Promise.all(d8Questions.map(q =>
                api.saveAnswer(parseInt(responseId), q.question_id, [])
            ));

            // Mark skipped as answered (or handled)
            const newAnswered = { ...answeredMap };
            d8Questions.forEach(q => newAnswered[q.question_id] = true);
            setAnsweredMap(newAnswered);

            let nextIndex = -1;
            for (let i = currentIndex + 1; i < questions.length; i++) {
                if (questions[i].dimension_id !== 8) {
                    nextIndex = i;
                    break;
                }
            }

            if (nextIndex !== -1) {
                setCurrentIndex(nextIndex);
                toast.info("Skipped remaining Dimension 8 questions.");
            } else {
                // Do NOT complete assessment yet. Navigate to Company Snapshot.
                toast.success("Questions complete! Just one last step.");
                navigate('/snapshot');
            }
        } catch (error) {
            console.error("Skip failed", error);
            if (error.message && (error.message.includes("404") || error.message.toLowerCase().includes("not found"))) {
                toast.error("Session expired. Please start over.");
                navigate('/');
                return;
            }
            toast.error(error.message || "Failed to skip dimension.");
        } finally {
            setSaving(false);
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-screen bg-slate-50 text-slate-500 font-medium animate-pulse">
            Loading assessment...
        </div>
    );

    if (!questions.length) return (
        <div className="flex justify-center items-center h-screen bg-slate-50 text-slate-500">
            No questions found.
        </div>
    );

    const currentQuestion = questions[currentIndex];
    const currentDimensionId = currentQuestion.dimension_id || 0;

    const renderAnswers = () => {
        const answers = currentQuestion.answers || [];
        const type = (currentQuestion.type || 'choice').toLowerCase();

        if (type === 'slider') {
            const maxIndex = answers.length - 1;
            const currentSelectedId = selectedAnswers[0];
            const currentIndexVal = answers.findIndex(a => a.answer_id === currentSelectedId);
            const safeIndex = currentIndexVal !== -1 ? currentIndexVal : 0;

            return (
                <div className="flex flex-col justify-center h-full px-4 md:px-8 py-4">
                    <div className="mb-4 text-center">
                        <motion.div
                            key={answers[safeIndex]?.answer_text}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="inline-block px-6 py-2 rounded-2xl bg-blue-50 text-blue-700 text-xl font-bold border border-blue-100 shadow-sm"
                        >
                            {answers[safeIndex]?.answer_text || "Drag to select"}
                        </motion.div>
                    </div>
                    <Slider
                        value={[safeIndex]}
                        max={maxIndex}
                        step={1}
                        onValueChange={handleSliderChange}
                        className="w-full cursor-pointer py-4"
                    />
                    <div className="flex justify-between mt-8 text-sm font-semibold text-slate-400 uppercase tracking-wider">
                        <span>{answers[0]?.answer_text}</span>
                        <span>{answers[maxIndex]?.answer_text}</span>
                    </div>
                </div>
            );
        }

        if (type === 'checklist') {
            return (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {answers.map(ans => (
                        <motion.div
                            key={ans.answer_id}
                            whileHover={{ scale: 1.005 }}
                            whileTap={{ scale: 0.995 }}
                            className={cn(
                                "flex items-start space-x-3 p-3 border rounded-xl cursor-pointer transition-all duration-200 h-full",
                                selectedAnswers.includes(ans.answer_id)
                                    ? "border-blue-600 bg-blue-50/50 shadow-md"
                                    : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 hover:shadow-sm"
                            )}
                            onClick={() => toggleCheckbox(ans.answer_id)}
                        >
                            <Checkbox
                                id={`ans-${ans.answer_id}`}
                                checked={selectedAnswers.includes(ans.answer_id)}
                                onCheckedChange={() => toggleCheckbox(ans.answer_id)}
                                className="mt-0.5 h-4 w-4 border-2 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 shrink-0"
                            />
                            <Label
                                htmlFor={`ans-${ans.answer_id}`}
                                className="text-[13px] font-medium leading-snug cursor-pointer flex-1 select-none text-slate-700"
                            >
                                {ans.answer_text}
                            </Label>
                        </motion.div>
                    ))}
                </div>
            );
        }

        // Default: Choice / Statement (Radio)
        const isShortText = answers.every(a => (a.answer_text || '').length < 60);

        return (
            <RadioGroup
                value={selectedAnswers[0]?.toString()}
                onValueChange={handleRadioChange}
                className={cn(
                    "w-full gap-1.5",
                    isShortText
                        ? "flex flex-col w-full"
                        : "grid grid-cols-1 md:grid-cols-2"
                )}
            >
                {answers.map(ans => (
                    <motion.div
                        key={ans.answer_id}
                        whileHover={{ scale: 1.005 }}
                        whileTap={{ scale: 0.995 }}
                        className={cn(
                            "flex space-x-3 border rounded-xl cursor-pointer transition-all duration-200 h-full",
                            isShortText ? "p-3 items-center" : "p-3 items-start",
                            selectedAnswers.includes(ans.answer_id)
                                ? "border-blue-600 bg-blue-50/50 shadow-md ring-1 ring-blue-600/20"
                                : "border-slate-200 bg-white hover:border-blue-300 hover:bg-slate-50 hover:shadow-sm"
                        )}
                        onClick={() => handleRadioChange(ans.answer_id.toString())}
                    >
                        <RadioGroupItem
                            value={ans.answer_id.toString()}
                            id={`ans-${ans.answer_id}`}
                            className="mt-0.5 h-4 w-4 border-2 text-blue-600 border-slate-300 data-[state=checked]:border-blue-600 shrink-0"
                        />
                        <Label
                            htmlFor={`ans-${ans.answer_id}`}
                            className="text-[13px] font-medium leading-snug flex-1 cursor-pointer select-none text-slate-700"
                        >
                            {ans.answer_text}
                        </Label>
                        {selectedAnswers.includes(ans.answer_id) && (
                            <CheckCircle2 className="w-4 h-4 text-blue-600 animate-in zoom-in spin-in-90 duration-300 shrink-0" />
                        )}
                    </motion.div>
                ))}
            </RadioGroup>
        );
    };

    const DimensionList = () => (
        <div className="space-y-2 py-1 w-full px-3">
            <div className="px-4 mb-3">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest bg-white/30 w-fit px-2 py-1 rounded-md backdrop-blur-sm">Your Progress</h3>
            </div>
            {dimensions.filter(d => d.id !== 8).map((dim, idx) => {
                const isActive = dim.id === currentDimensionId;
                const isCompleted = dim.answered === dim.total;
                const progress = (dim.answered / dim.total) * 100;

                return (
                    <div key={dim.id} className={cn(
                        "relative px-3 py-1 flex items-center gap-3 transition-all duration-500 rounded-xl mx-2 group",
                        isActive
                            ? "glass-premium translate-x-1"
                            : "bg-slate-50/50 hover:bg-slate-100/50 hover:translate-x-1"
                    )}>
                        {/* Active Indicator Color Splash */}
                        {isActive && (
                            <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-purple-500/5 rounded-2xl pointer-events-none" />
                        )}
                        {/* Active Line */}
                        {isActive && (
                            <div className="absolute left-0 top-1/2 -translate-y-1/2 h-8 w-1 bg-gradient-to-b from-indigo-500 to-violet-600 rounded-r-full shadow-[0_0_12px_rgba(99,102,241,0.6)]" />
                        )}

                        <div className="flex-none relative z-10">
                            {isCompleted ? (
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white shadow-lg shadow-emerald-500/30 ring-2 ring-white/80">
                                    <Check className="w-5 h-5" />
                                </div>
                            ) : isActive ? (
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-xl shadow-indigo-500/40 ring-2 ring-white animate-pulse-slow">
                                    <Disc className="w-5 h-5" />
                                </div>
                            ) : (
                                <div className="w-10 h-10 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-500 group-hover:bg-slate-200 group-hover:shadow-sm transition-all">
                                    <span className="text-xs font-bold font-heading">{idx + 1}</span>
                                </div>
                            )}
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className={cn("text-sm font-bold truncate mb-1 transition-colors", isActive ? "text-slate-800" : "text-slate-500 group-hover:text-slate-700")}>
                                {dim.name}
                            </div>
                            <div className="flex items-center gap-3">
                                <Progress
                                    value={progress}
                                    className="h-1.5 bg-slate-200 flex-1"
                                    indicatorClassName={isCompleted ? "bg-emerald-500" : isActive ? "bg-gradient-to-r from-indigo-500 to-violet-500" : "bg-slate-400"}
                                />
                                <span className={cn("text-[10px] font-semibold tabular-nums", isActive ? "text-indigo-600" : "text-slate-400")}>
                                    {Math.round(progress)}%
                                </span>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );

    return (
        <div className="h-screen w-screen overflow-hidden flex relative font-sans">
            <PageBackground />

            {/* Desktop Sidebar */}
            <aside className="hidden lg:flex flex-col w-96 bg-white/10 backdrop-blur-3xl border-r border-white/20 z-20 h-full overflow-y-auto custom-scrollbar shadow-[20px_0_40px_rgba(0,0,0,0.02)]">
                <div className="p-6 pb-2">
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20 ring-2 ring-white/10">
                            <Compass className="w-6 h-6 text-white" />
                        </div>
                        <div className="flex flex-col justify-center">
                            <div className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent font-heading tracking-tight leading-none">
                                AI Compass
                            </div>
                        </div>
                    </div>
                </div>
                <DimensionList />
            </aside>

            {/* Mobile Header with Drawer */}
            <div className="lg:hidden absolute top-0 left-0 w-full glass-premium z-30 flex justify-between items-center px-4 py-3">
                <div className="font-bold text-slate-800 truncate max-w-[200px]">
                    {currentQuestion.dimension_name}
                </div>
                <Sheet>
                    <SheetTrigger asChild>
                        <Button variant="ghost" size="icon" className="hover:bg-white/20">
                            <Menu className="w-6 h-6 text-slate-600" />
                        </Button>
                    </SheetTrigger>
                    <SheetContent side="left" className="w-80 p-0 bg-white/95 backdrop-blur-xl">
                        <div className="p-6 border-b border-slate-100">
                            <div className="text-xl font-bold text-slate-900">Dimensions</div>
                        </div>
                        <DimensionList />
                    </SheetContent>
                </Sheet>
            </div>

            {/* Main Content Area */}
            <main className="flex-1 flex flex-col h-full relative z-10 pt-16 lg:pt-0 overflow-hidden">
                <div className="flex-1 flex flex-col w-full h-full max-w-3xl mx-auto p-1 md:p-2 justify-center overflow-hidden">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={currentIndex}
                            initial={{ opacity: 0, scale: 0.98, y: 10 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 1.02 }}
                            transition={{ duration: 0.4, ease: [0.19, 1.0, 0.22, 1.0] }} // Authentic iOS ease
                            className="w-full flex flex-col h-full max-h-full"
                        >
                            <Card className="flex flex-col glass-premium rounded-[1.5rem] overflow-hidden w-full h-full max-h-full border-white/50 ring-1 ring-white/60">
                                {/* Question Header */}
                                <CardHeader className="flex-none border-b border-white/20 bg-white/20 pb-0 pt-3 px-4 md:px-6 backdrop-blur-md">
                                    <div className="flex items-center justify-between mb-0.5">
                                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/50 border border-white/60 shadow-sm text-indigo-900 text-[10px] font-bold uppercase tracking-widest backdrop-blur-sm">
                                            <span className="relative flex h-1.5 w-1.5 mr-0.5">
                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                                                <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-indigo-600"></span>
                                            </span>
                                            Question {currentIndex + 1} / {questions.length}
                                        </div>
                                    </div>

                                    <CardTitle className="text-[15px] font-black text-slate-800 tracking-tight font-heading leading-tight mb-1">
                                        {(() => {
                                            const text = currentQuestion.question_text;
                                            const parts = text.split('(Select all that apply)');
                                            if (parts.length > 1) {
                                                return (
                                                    <>
                                                        {parts[0]}
                                                        <span className="font-normal text-slate-500">(Select all that apply)</span>
                                                        {parts[1]}
                                                    </>
                                                );
                                            }
                                            return text;
                                        })()}
                                    </CardTitle>
                                </CardHeader>

                                {/* Answers Area */}
                                <CardContent className="flex-1 overflow-y-auto px-4 py-0 md:px-6 custom-scrollbar">
                                    <div className="max-w-3xl mx-auto h-full flex flex-col gap-1.5 pt-2">
                                        {renderAnswers()}
                                    </div>
                                </CardContent>

                                {/* Persistent Footer */}
                                <CardFooter className="flex-none border-t border-slate-100/50 bg-white/40 px-4 py-1.5 md:px-6 backdrop-blur-md">
                                    <div className="flex justify-between w-full items-center">
                                        <div className="flex gap-4">
                                            <Button
                                                variant="outline"
                                                disabled={currentIndex === 0}
                                                onClick={() => setCurrentIndex(prev => prev - 1)}
                                                className="border-slate-300 text-slate-600 hover:text-slate-900 hover:bg-slate-100/50 px-3 h-9 text-xs rounded-lg transition-all hover:border-slate-400"
                                            >
                                                <ChevronLeft className="w-3 h-3 mr-1" />
                                                Back
                                            </Button>
                                            {currentQuestion.dimension_id === 8 && (
                                                <Button
                                                    variant="outline"
                                                    onClick={handleSkipDimension}
                                                    disabled={saving}
                                                    className="border-amber-200 text-amber-700 hover:text-amber-800 hover:bg-amber-50 px-3 h-9 text-xs rounded-lg transition-all hover:border-amber-300"
                                                >
                                                    <SkipForward className="w-3 h-3 mr-2" />
                                                    Skip Section
                                                </Button>
                                            )}
                                        </div>

                                        <div className="flex items-center gap-6">
                                            {saving && <span className="text-xs font-medium text-indigo-600 animate-pulse hidden sm:inline-block">Saving...</span>}
                                            <Button
                                                size="lg"
                                                onClick={handleNext}
                                                disabled={saving || selectedAnswers.length === 0}
                                                className="relative px-5 h-10 text-sm font-bold rounded-xl transition-all shadow-[0_4px_10px_-2px_rgba(79,70,229,0.5)] active:scale-95 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white border-0 ring-1 ring-white/20 overflow-hidden group"
                                            >
                                                {/* Shimmer Effect */}
                                                <div className="absolute inset-0 -translate-x-full group-hover:animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/20 to-transparent z-10" />

                                                <span className="relative z-20 flex items-center font-bold tracking-wide">
                                                    {currentIndex === questions.length - 1 ? 'Finish' : 'Next'}
                                                    {!saving && (currentIndex === questions.length - 1 ? <CheckCircle2 className="w-4 h-4 ml-2" /> : <ArrowRight className="w-4 h-4 ml-2" />)}
                                                </span>
                                            </Button>
                                        </div>
                                    </div>
                                </CardFooter>

                            </Card>
                        </motion.div>
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
}
