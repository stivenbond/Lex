using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
// ReSharper disable PropertyCanBeMadeInitOnly.Global

namespace Lex.Models
{
    public class Lesson
    {
        public int LessonId { get; set; }

        [Required, MaxLength(255)]
        public string Topic { get; set; } = string.Empty;

        public int Year { get; set; }

        [Required, MaxLength(255)]
        public string Subject { get; set; } = string.Empty;

        [Required]
        // ReSharper disable once EntityFramework.ModelValidation.UnlimitedStringLength
        public string Content { get; set; } = string.Empty; // Stored as TEXT via Fluent API

        public ICollection<Test> Tests { get; set; } = new List<Test>();
        public ICollection<LessonFile> Files { get; set; } = new List<LessonFile>();
    }

    public class Test
    {
        public int TestId { get; set; }

        public int LessonId { get; set; }

        [ForeignKey("LessonId")]
        public Lesson Lesson { get; set; } = null!;

        public ICollection<Question> Questions { get; set; } = new List<Question>();
    }

    public class Question
    {
        public int QuestionId { get; set; }

        public int TestId { get; set; }

        [ForeignKey("TestId")]
        public Test Test { get; set; } = null!;

        [Required, MaxLength(512)]
        public string QuestionText { get; set; } = string.Empty;

        [Required, MaxLength(512)]
        public string OptionA { get; set; } = string.Empty;

        [Required, MaxLength(512)]
        public string OptionB { get; set; } = string.Empty;

        [Required, MaxLength(512)]
        public string OptionC { get; set; } = string.Empty;

        [Required, MaxLength(512)]
        public string OptionD { get; set; } = string.Empty;

        [Required]
        public char CorrectOption { get; set; } // A, B, C, or D
    }

    public class LessonFile
    {
        public int FileId { get; set; }

        public int LessonId { get; set; }

        [ForeignKey("LessonId")]
        public Lesson Lesson { get; set; } = null!;

        [Required]
        public byte[] Content { get; set; } = [];

        [Required, MaxLength(255)]
        public string Type { get; set; } = string.Empty; // e.g. "image/png"
    }

    public class Diary
    {
        public int DiaryId { get; set; }

        [Required]
        // ReSharper disable once EntityFramework.ModelValidation.UnlimitedStringLength
        public string Content { get; set; } = string.Empty; // Stored as TEXT via Fluent API

        public bool SentOver { get; set; }

        public int ClassToReference { get; set; }

        [ForeignKey("ClassToReference")]
        public SchoolClass Class { get; set; } = null!;

        public DateTime DateOfReference { get; set; }
    }

    public class SchoolClass
    {
        public int ClassId { get; set; }

        public int Year { get; set; }

        public int Index { get; set; }

        [Required, MaxLength(255)]
        public string Subject { get; set; } = string.Empty;

        public int? CurrentLessonId { get; set; }

        [ForeignKey("CurrentLessonId")]
        public Lesson? CurrentLesson { get; set; }

        public ICollection<Diary> Diaries { get; set; } = new List<Diary>();
    }
}
