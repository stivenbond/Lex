using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Lex.Models;

public class Lesson
{
    [Key]
    public int LessonId { get; set; }

    public required string Topic { get; set; }
    public required int Year { get; set; }
    public required string Subject { get; set; }

    public required string Content { get; set; } // JSON stored as string

    public required ICollection<Test> Tests { get; set; }
    public required ICollection<File> Files { get; set; }
    public required ICollection<Class> Classes { get; set; }
}
