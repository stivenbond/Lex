using Avalonia;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Lex.ViewModels;
using Microsoft.Extensions.DependencyInjection;

namespace Lex.Views
{
    public partial class LeftSidebarView : UserControl
    {
        public LeftSidebarView(LeftSidebarViewModel viewModel)
        {
            InitializeComponent();
            DataContext = viewModel;
        }

        public LeftSidebarView()
        {
            InitializeComponent();
        }

        
        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }

        // If you use a separate ViewModel, you might set the DataContext here or in the MainView,
        // For example,
        // public LeftSidebarView(LeftSidebarViewModel viewModel)
        // {
        //     InitializeComponent();
        //     DataContext = viewModel;
        // }
    }
}