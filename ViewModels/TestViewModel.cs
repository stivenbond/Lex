using System.Collections.ObjectModel;
using ReactiveUI;

namespace Lex.ViewModels
{
    public class TestViewModel : ViewModelBase
    {
        public required ObservableCollection<TestQuestionViewModel> _questions;
        public ObservableCollection<TestQuestionViewModel> Questions
        {
            get => _questions;
            set => this.RaiseAndSetIfChanged(ref _questions, value);
        }

        public TestViewModel()
        {
            Questions = new ObservableCollection<TestQuestionViewModel>
            {
                new TestQuestionViewModel
                {
                    QuestionText = "Sample test question 1?",
                    Options = new ObservableCollection<string>
                    {
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D"
                    },
                    _questionText = null,
                    _options = null
                },
                new TestQuestionViewModel
                {
                    QuestionText = "Sample test question 2?",
                    Options = new ObservableCollection<string>
                    {
                        "Option A",
                        "Option B",
                        "Option C",
                        "Option D"
                    },
                    _questionText = null,
                    _options = null
                }
            };
        }
    }

    public class TestQuestionViewModel : ViewModelBase
    {
        public required string _questionText;
        public string QuestionText
        {
            get => _questionText;
            set => this.RaiseAndSetIfChanged(ref _questionText, value);
        }

        public required ObservableCollection<string> _options;
        public ObservableCollection<string> Options
        {
            get => _options;
            set => this.RaiseAndSetIfChanged(ref _options, value);
        }

        private int _selectedOptionIndex = -1;
        public int SelectedOptionIndex
        {
            get => _selectedOptionIndex;
            set => this.RaiseAndSetIfChanged(ref _selectedOptionIndex, value);
        }
    }
}