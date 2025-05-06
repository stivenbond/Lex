using System.Collections.ObjectModel;
using ReactiveUI;
using System.Reactive;

namespace Lex.ViewModels
{
    public class SlideshowViewModel : ViewModelBase
    {
        public required ObservableCollection<SlideViewModel> _slides;
        public ObservableCollection<SlideViewModel> Slides
        {
            get => _slides;
            set => this.RaiseAndSetIfChanged(ref _slides, value);
        }

        private int _currentSlideIndex;
        public int CurrentSlideIndex
        {
            get => _currentSlideIndex;
            set => this.RaiseAndSetIfChanged(ref _currentSlideIndex, value);
        }

        public SlideViewModel CurrentSlide => Slides.Count > 0 ? Slides[CurrentSlideIndex] : null;

        public ReactiveCommand<Unit, Unit> NextSlideCommand { get; }
        public ReactiveCommand<Unit, Unit> PreviousSlideCommand { get; }

        public SlideshowViewModel()
        {
            Slides = new ObservableCollection<SlideViewModel>
            {
                new SlideViewModel
                {
                    Content = "Slide 1 Content",
                    _content = null
                },
                new SlideViewModel
                {
                    Content = "Slide 2 Content",
                    _content = null
                },
                new SlideViewModel
                {
                    Content = "Slide 3 Content",
                    _content = null
                }
            };

            CurrentSlideIndex = 0;

            NextSlideCommand = ReactiveCommand.Create(() =>
            {
                if (CurrentSlideIndex < Slides.Count - 1)
                {
                    CurrentSlideIndex++;
                    this.RaisePropertyChanged(nameof(CurrentSlide));
                }
            });

            PreviousSlideCommand = ReactiveCommand.Create(() =>
            {
                if (CurrentSlideIndex > 0)
                {
                    CurrentSlideIndex--;
                    this.RaisePropertyChanged(nameof(CurrentSlide));
                }
            });
        }
    }

    public class SlideViewModel : ViewModelBase
    {
        public required string _content;
        public string Content
        {
            get => _content;
            set => this.RaiseAndSetIfChanged(ref _content, value);
        }
    }
}