using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Lex.Models;

public class Question
{
    [Key]
    public int QuestionId { get; set; }

    public int TestId { get; set; }
    [ForeignKey("TestId")]
    public required Test Test { get; set; }

    public required string QuestionText { get; set; }
    public required string OptionA { get; set; }
    public required string OptionB { get; set; }
    public required string OptionC { get; set; }
    public required string OptionD { get; set; }

    public char CorrectOption { get; set; }
}