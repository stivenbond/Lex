using System;
using System.Collections.ObjectModel;
using Lex.Models;
using Lex.Data.Repositories;
using ReactiveUI;
using DynamicData;
namespace Lex.ViewModels;

public class LeftSidebarViewModel : ReactiveObject
{
    private ReadOnlyObservableCollection<Lesson> _lessonTopics;
    public ReadOnlyObservableCollection<Lesson> LessonTopics
    {
        get => _lessonTopics;
        set => this.RaiseAndSetIfChanged(ref _lessonTopics, value);
    }

    private Lesson? _selectedLessonTopic;
    public Lesson? SelectedLessonTopic
    {
        get => _selectedLessonTopic;
        set => this.RaiseAndSetIfChanged(ref _selectedLessonTopic, value);
    }

    public LeftSidebarViewModel(LessonRepository lessonRepo)
    {
        lessonRepo.Connect()
            .Bind(out _lessonTopics)
            .Subscribe();

        lessonRepo.GetAllAsync().Wait();
    }
    
}