using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Lex.Models;

public class Test
{
    [Key]
    public int TestId { get; set; }

    public int LessonId { get; set; }
    [ForeignKey("LessonId")]
    public required  Lesson Lesson { get; set; }

    public required ICollection<Question> Questions { get; set; }
}